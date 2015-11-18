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

        logging.info("Loading datasets[1]...")

        with open(self.data_dir / 'beer' / 'beer-core.pkl', 'rb') as fp:
            beer_core = pickle.load(fp)[0]

        self.top_encoding = OneHotEncoding(include_start_token=True,
                                           include_stop_token=True)
        self.core_encoding = OneHotEncoding(include_start_token=True,
                                           include_stop_token=True)
        top_sequences = [CharacterSequence.from_string(r.text) for r in beer_top]
        self.top_encoding.build_encoding(top_sequences)

        core_sequences = [CharacterSequence.from_string(r.text) for r in beer_core]
        self.core_encoding.build_encoding(core_sequences)

        top_cats = [SingletonSequence(r.beer.style) for r in beer_top]

        self.cat_encoding = OneHotEncoding(include_start_token=False,
                                           include_stop_token=False)
        self.cat_encoding.build_encoding(top_cats)
        self.rat_encoding = IdentityEncoding(1)

        logging.info("Loading models[0]...")

        self.ratnet = CharacterRNN('ratnet',
                                   len(self.core_encoding) + len(self.rat_encoding),
                                   len(self.core_encoding),
                                   n_layers=2,
                                   n_hidden=1024)
        self.ratnet.load_parameters(self.model_dir / 'ratnet.pkl')
        self.ratnet.compile_method('generate_with_concat')
        self.ratnet.compile_method('log_probability')

        logging.info("Loading models[1]...")
        self.catnet = CharacterRNN('catnet',
                                   len(self.top_encoding) + len(self.cat_encoding),
                                   len(self.top_encoding),
                                   n_layers=2,
                                   n_hidden=1024)
        self.catnet.load_parameters(self.model_dir / 'catnet.pkl')
        self.catnet.compile_method('generate_with_concat')
        self.catnet.compile_method('log_probability')

    def generate_rating(self, rating, length, temperature=1.0):
        rating = self.transform_rating(rating)
        results = self.ratnet.generate_with_concat(
            np.eye(len(self.core_encoding))[self.core_encoding.encode("<STR>")],
            [rating],
            length,
            temperature
        )
        return str(NumberSequence(results.argmax(axis=1)).decode(self.core_encoding))

    def generate_category(self, category, length, temperature=1.0):
        results = self.catnet.generate_with_concat(
            np.eye(len(self.top_encoding))[self.top_encoding.encode("<STR>")],
            np.eye(len(self.cat_encoding))[self.cat_encoding.encode(category)],
            length,
            temperature
        )
        return str(NumberSequence(results.argmax(axis=1)).decode(self.top_encoding))

    def transform_rating(self, rating):
        return (rating - 3.0) / 2.0

    def inverse_transform_rating(self, rating):
        return rating * 2 + 3
