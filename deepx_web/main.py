import logging
logging.basicConfig(level=logging.DEBUG, filename='server.log')
from server import Server
from argparse import ArgumentParser

def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument('--host', default='0.0.0.0')
    argparser.add_argument('--model_dir', default='models/')
    argparser.add_argument('--data_dir', default='data/')
    argparser.add_argument('--port', type=int, default=1337)
    argparser.add_argument('--no_beermind', dest='run_beermind', action='store_false')
    argparser.add_argument('--ddc_rpc_port', type=int, default=13337)
    argparser.add_argument('--ddc_audio_upload_dir', default='/data1/ddc_bulk/audio')
    argparser.set_defaults(run_beermind=True)

    return argparser.parse_args()

def main():
    args = parse_args()

    server = Server(args.host,
                    args.port,
                    args.model_dir,
                    args.data_dir,
                    run_beermind=args.run_beermind,
                    ddc_rpc_port=args.ddc_rpc_port,
                    ddc_audio_upload_dir=args.ddc_audio_upload_dir)
    server.initialize()
    logging.info("Server running...")
    server.listen()
