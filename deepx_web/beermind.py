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
        top_sequences = [CharacterSequence.from_string(r.text) for r in beer_top]
        self.top_encoding.build_encoding(top_sequences)

        top_cats = [SingletonSequence(r.beer.style) for r in beer_top]

        self.cat_encoding = OneHotEncoding(include_start_token=False,
                                           include_stop_token=False)
        self.cat_encoding.build_encoding(top_cats)
        self.rat_encoding = IdentityEncoding(1)

        self.core_encoding = OneHotEncoding(include_start_token=True,
                                           include_stop_token=True)
        core_sequences = [CharacterSequence.from_string(r.text) for r in beer_core]
        self.core_encoding.build_encoding(core_sequences)

        core_users = [SingletonSequence(r.user) for r in beer_core]
        self.user_encoding = OneHotEncoding(include_start_token=False,
                                           include_stop_token=False)
        self.user_encoding.build_encoding(core_users)

        core_items = [SingletonSequence(r.beer.name) for r in beer_core]
        self.item_encoding = OneHotEncoding(include_start_token=False,
                                           include_stop_token=False)
        self.item_encoding.build_encoding(core_items)

        logging.info("Loading models[0]...")

        self.catnet = CharacterRNN('catnet',
                                      len(self.top_encoding) + len(self.cat_encoding),
                                      len(self.top_encoding),
                                      n_layers=2,
                                      n_hidden=1024)
        self.catnet.load_parameters(self.model_dir / 'catnet.pkl')
        self.catnet.compile_method('log_probability')

        self.catratnet = CharacterRNN('catratnet',
                                      len(self.top_encoding) + len(self.rat_encoding) + len(self.cat_encoding),
                                      len(self.top_encoding),
                                      n_layers=2,
                                      n_hidden=1024)
        self.catratnet.load_parameters(self.model_dir / 'catratnet.pkl')
        self.catratnet.compile_method('generate_with_concat')

        logging.info("Loading models[1]...")
        self.useritemnet = CharacterRNN('useritemnet',
                                      len(self.core_encoding) + len(self.user_encoding) + len(self.item_encoding),
                                      len(self.core_encoding),
                                      n_layers=2,
                                      n_hidden=1024)
        self.useritemnet.load_parameters(self.model_dir / 'useritemnet.pkl')
        self.useritemnet.compile_method('generate_with_concat')

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

    def category_probability(self, review):
        num_review = CharacterSequence(review).encode(self.cat_encoding).seq.ravel()
        Xs = num_review[:-1]
        idx = num_review[1:]
        return str(NumberSequence(results.argmax(axis=1)).decode(self.top_encoding))

    def users(self):
        return self.user_encoding.backward_mapping

    def items(self):
        return self.item_encoding.backward_mapping

    def generate_useritemnet(self, user, item, length, temperature=1.0):
        results = self.useritemnet.generate_with_concat(
            np.eye(len(self.core_encoding))[self.top_encoding.encode("<STR>")],
            np.concatenate([np.eye(len(self.user_encoding))[self.user_encoding.encode(user)],
                            np.eye(len(self.item_encoding))[self.item_encoding.encode(item)]
                           ]),
            length,
            temperature
        )
        return str(NumberSequence(results.argmax(axis=1)).decode(self.core_encoding))

    def transform_rating(self, rating):
        return (rating - 3.0) / 2.0

    def inverse_transform_rating(self, rating):
        return rating * 2 + 3
