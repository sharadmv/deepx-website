from path import Path
from util import jsonp
from flask import Flask, jsonify, redirect
from beermind import Beermind
from webargs import fields
from webargs.flaskparser import use_args

class Server(object):

    def __init__(self, host, port, model_dir, data_dir):
        self.host = host
        self.port = port
        self.model_dir = Path(model_dir)
        self.data_dir = Path(data_dir)

        self.app = Flask(__name__, static_url_path='', static_folder='static/')

        self.beermind = Beermind(self.model_dir,
                                 self.data_dir)


    def listen(self):
        self.app.run(host=self.host,
                        port=self.port)

    def initialize(self):
        self.initialize_static_routes()
        self.initialize_api_routes()
        self.initialize_beermind()

    def initialize_static_routes(self):

        @self.app.route('/')
        def index():
            return self.app.send_static_file('index.html')

        @self.app.route('/beermind')
        def beermind():
            return redirect('/#/home/beermind')

    def initialize_api_routes(self):
        pass

    def initialize_beermind(self):

        @jsonp
        @self.app.route('/api/beermind/generate_rating')
        @use_args({
            'rating': fields.Float(required=True,
                                   validate=lambda val: val >= 0.0 and val <= 10.0),
            'temperature': fields.Float(missing=0.5),
        })
        def generate_rating(args):
            results = self.beermind.generate_rating(args['rating'], 2000, temperature=args['temperature'])
            results = results.split("<EOS>")[0]
            return jsonify({
                'results': results
            })

        @jsonp
        @self.app.route('/api/beermind/generate_category')
        @use_args({
            'category': fields.Str(required=True),
            'temperature': fields.Float(missing=0.5),
        })
        def generate_category(args):
            if args['category'] not in self.beermind.cat_encoding.backward_mapping:
                return jsonify({
                    'results': ""
                })
            results = self.beermind.generate_category(args['category'], 2000, temperature=args['temperature'])
            results = results.split("<EOS>")[0]
            return jsonify({
                'results': results
            })
