import numpy as np
import logging
import cPickle as pickle

from deepx.dataset import OneHotEncoding, IdentityEncoding
from deepx.dataset import SingletonSequence, CharacterSequence, NumberSequence
from deepx.sequence import CharacterRNN

class Beermind(object):

    def __init__(self, model_dir, data_dir):
        self.model_dir = model_dir
        self.data_dir = data_dir

        logging.info("Loading datasets[0]...")

        with open(self.data_dir / 'beer' / 'beer-top.pkl', 'rb') as fp:
            beer_top = pickle.load(fp)[0]

        self.top_encoding = OneHotEncoding(include_start_token=True,
                                           include_stop_token=True)
        top_sequences = [CharacterSequence.from_string(r.text) for r in beer_top]
        self.top_encoding.build_encoding(top_sequences)

        top_cats = [SingletonSequence(r.beer.style) for r in beer_top]

        self.cat_encoding = OneHotEncoding(include_start_token=False,
                                           include_stop_token=False)
        self.cat_encoding.build_encoding(top_cats)
        self.rat_encoding = IdentityEncoding(1)

        logging.info("Loading models[0]...")

        self.catratnet = CharacterRNN('catratnet',
                                      len(self.top_encoding) + len(self.rat_encoding) + len(self.cat_encoding),
                                      len(self.top_encoding),
                                      n_layers=2,
                                      n_hidden=1024)
        self.catratnet.load_parameters(self.model_dir / 'catratnet.pkl')
        self.catratnet.compile_method('generate_with_concat')

    def generate(self, category, rating, length, temperature=1.0):
        rating = self.transform_rating(rating)
        results = self.catratnet.generate_with_concat(
            np.eye(len(self.top_encoding))[self.top_encoding.encode("<STR>")],
            np.concatenate([np.eye(len(self.cat_encoding))[self.cat_encoding.encode(category)],
                            [rating]]),
            length,
            temperature
        )
        return str(NumberSequence(results.argmax(axis=1)).decode(self.top_encoding))

    def transform_rating(self, rating):
        return (rating - 3.0) / 2.0

    def inverse_transform_rating(self, rating):
        return rating * 2 + 3
