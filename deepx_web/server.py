from util import jsonp
from flask import Flask

class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.app = Flask(__name__, static_url_path='', static_folder='static/')

    def listen(self):
        self.app.run(host=self.host,
                        port=self.port)

    def initialize(self):
        self.initialize_static_routes()
        self.initialize_api_routes()

    def initialize_static_routes(self):

        @self.app.route('/')
        def index():
            return self.app.send_static_file('index.html')

    def initialize_api_routes(self):
        pass
