import pickle
from ir.p3.data.spimi_block import Block


def write_to_pickle(block, block_name):
    with open(block_name, 'wb+') as pickle_file:
        pickle.dump(block, pickle_file, pickle.HIGHEST_PROTOCOL)
        return pickle_file


def load_block_from_pickle(path) -> Block:
    return pickle.load(open(path, "rb"))
