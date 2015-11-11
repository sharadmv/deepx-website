from server import Server
from argparse import ArgumentParser

def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument('--host', default='0.0.0.0')
    argparser.add_argument('--port', type=int, default=1337)

    return argparser.parse_args()

def main():
    args = parse_args()

    server = Server(args.host,
                    args.port)
    server.initialize()
    server.listen()
