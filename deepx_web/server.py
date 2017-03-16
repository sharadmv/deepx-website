import tornado
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import random
import os
from path import Path
from util import jsonp
from flask import Flask, jsonify, redirect, request, flash, url_for, flash, render_template, send_file
import sqlite3 as sql
from webargs import fields
from webargs.flaskparser import use_args
from werkzeug.utils import secure_filename
import xmlrpclib
from keys import FLASK_SECRET_KEY 

tornado.log.enable_pretty_logging()

class Server(object):

    def __init__(self, host, port, model_dir, data_dir, db_fp, run_beermind=True, ddc_rpc_port=13337, ddc_audio_upload_dir=None):
        self.host = host
        self.port = port
        self.model_dir = Path(model_dir)
        self.data_dir = Path(data_dir)
        self.db_fp = db_fp

        self.app = Flask(__name__, static_url_path='', static_folder='static/')
        self.app.secret_key = FLASK_SECRET_KEY

        self.app.config['DDC_AUDIO_FILES_DIR'] = ddc_audio_upload_dir
        self.app.config['DDC_ALLOWED_EXTENSIONS'] = set(['mp3', 'ogg', 'aiff', 'wav'])

        if run_beermind:
            from beermind import Beermind
            self.beermind = Beermind(self.model_dir,
                                 self.data_dir)
        self.ddc = xmlrpclib.ServerProxy('http://localhost:{}'.format(ddc_rpc_port))


    def listen(self):
        http_server = HTTPServer(WSGIContainer(self.app))
        http_server.listen(self.port)
        IOLoop.instance().start()

    def initialize(self):
        self.initialize_static_routes()
        self.initialize_api_routes()
        self.initialize_beermind()
        self.initialize_ddc()

    def initialize_static_routes(self):

        @self.app.route('/')
        def index():
            return self.app.send_static_file('index.html')

        @self.app.route('/beermind')
        def beermind():
            return redirect('/#/home/beermind')

        @self.app.route('/ddc')
        def ddc():
            return render_template('ddc.html')

    def initialize_api_routes(self):
        pass

    def initialize_beermind(self):

        @jsonp
        @self.app.route('/api/beermind/generate')
        @use_args({
            'rating': fields.Float(missing=-1),
            'category': fields.Str(missing=None),
            'temperature': fields.Float(missing=0.5),
        })
        def generate(args):
            category = random.choice(self.beermind.cat_encoding.backward_mapping) if not args['category'] else args['category']
            rating = random.uniform(1, 5) if args['rating'] == -1 else args['rating']

            rating = max(rating, 0)
            rating = min(rating, 10)
            results = self.beermind.generate(category, rating, 2000, temperature=args['temperature'])
            results = results.split("<EOS>")[0]
            return jsonify({
                'results': results
            })

        @self.app.route('/api/beermind/category_probability')
        @use_args({
            'review': fields.Str(missing=None),
        })
        @jsonp
        def category_probability(args):
            review = args['review']
            results = self.beermind.category_probability(review)
            return jsonify({
                'results': results
            })

        @jsonp
        @self.app.route('/api/beermind/users')
        def users():
            return jsonify({
                'results': self.beermind.users()
            })

        @jsonp
        @self.app.route('/api/beermind/items')
        def items():
            return jsonify({
                'results': self.beermind.items()
            })

        @jsonp
        @self.app.route('/api/beermind/generate_useritemnet')
        @use_args({
            'user': fields.Str(missing=None),
            'item': fields.Str(missing=None),
            'temperature': fields.Float(missing=0.5),
        })
        def generate_useritemnet(args):
            user = args['user']
            item = args['item']

            results = self.beermind.generate_useritemnet(user, item, 2000, temperature=args['temperature'])
            results = results.split("<EOS>")[0]
            return jsonify({
                'results': results
            })

    _DDC_DIFFICULTIES = ['Beginner', 'Easy', 'Medium', 'Hard', 'Challenge']
    def initialize_ddc(self):
        @self.app.route('/api/ddc/choreograph', methods=['POST'])
        def ddc_choreograph():
            ip = request.remote_addr
            if request.content_length > 16 * 1024 * 1024:
                flash('Audio file too large', 'choreograph')
                return redirect(url_for('ddc'))

            uploaded_file = request.files.get('audio_file')
            if not uploaded_file:
                flash('Audio file required', 'choreograph')
                return redirect(url_for('ddc'))

            song_artist = request.form.get('song_artist', '')[:1024]
            song_title = request.form.get('song_title', '')[:1024]

            diff_coarse = request.form.get('diff_coarse')
            if diff_coarse not in self._DDC_DIFFICULTIES:
                flash('Difficulty required', 'choreograph')
                return redirect(url_for('ddc'))

            allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1].lower() in self.app.config['DDC_ALLOWED_EXTENSIONS']

            if allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)[:1024]
                audio_fp = os.path.join(self.app.config['DDC_AUDIO_FILES_DIR'], filename)
                uploaded_file.save(audio_fp)

                try:
                    zip_fp = self.ddc.create_chart(song_artist, song_title, audio_fp, [diff_coarse])
                except Exception as e:
                    msg = e.faultString.split(':', 1)[1]
                    flash(msg, 'choreograph')
                    return redirect(url_for('ddc'))

                uuid = os.path.splitext(os.path.split(zip_fp)[1])[0]
                with sql.connect(self.db_fp) as db_con:
                  db_cur = db_con.cursor()
                  db_cur.execute("INSERT INTO ddc_choreograph (ip,uuid,song_artist,song_title,diff_coarse,filename) VALUES (?,?,?,?,?,?)", (ip, uuid, song_artist, song_title, diff_coarse, filename))
                  db_con.commit()

                return send_file(zip_fp, as_attachment=True)
            else:
                flash('Invalid file type', 'choreograph')
                return redirect(url_for('ddc'))

        @self.app.route('/api/ddc/feedback', methods=['POST'])
        def ddc_feedback():
            ip = request.remote_addr
            email = request.form.get('email')
            satisfaction = request.form.get('satisfaction', -1)
            comments = request.form.get('comments')
            if not (email or satisfaction or comments):
                flash('No feedback provided', 'feedback')
                return redirect(url_for('ddc'))

            if len(email) > 1024:
                flash('Email too long', 'feedback')
                return redirect(url_for('ddc'))

            try:
                satisfaction = int(satisfaction)
            except:
                flash('Invalid satisfaction', 'feedback')
                return redirect(url_for('ddc'))
            if satisfaction not in [-1] + range(1,6):
                flash('Invalid satisfaction', 'feedback')
                return redirect(url_for('ddc'))

            if len(comments) > 8192:
                flash('Comments too long', 'feedback')
                return redirect(url_for('ddc'))

            with sql.connect(self.db_fp) as db_con:
              db_cur = db_con.cursor()
              db_cur.execute("INSERT INTO ddc_feedback (ip,email,satisfaction,comments) VALUES (?,?,?,?)", (ip, email, satisfaction, comments))
              db_con.commit()

            flash('Thanks for your feedback!', 'feedback')
            return redirect(url_for('ddc'))
