import tornado
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import random
from path import Path
from util import jsonp
from flask import Flask, jsonify, redirect
from beermind import Beermind
from webargs import fields
from webargs.flaskparser import use_args

tornado.log.enable_pretty_logging()

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
        http_server = HTTPServer(WSGIContainer(self.app))
        http_server.listen(self.port)
        IOLoop.instance().start()

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

        @jsonp
        @self.app.route('/api/beermind/category_probability')
        @use_args({
            'review': fields.Str(missing=None),
        })
        def category_probability(args):
            review = args['review']
            results = self.beermind.log_probability()
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
