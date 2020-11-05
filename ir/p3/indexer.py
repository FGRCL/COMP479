import pickle
from ir.p3.spimi_block import Block


def build_index(token_stream, max_dictionary_size, block_path):
    count = 0
    token_accumulator = []
    block_names = block_name_generator(block_path)
    blocks = []
    for token in token_stream:
        count += 1
        token_accumulator.append(token)
        if count == max_dictionary_size:
            block = build_block(token_accumulator)
            blocks.append(block)
            write_to_pickle(block, next(block_names))
            count = 0
            token_accumulator = []

    block = build_block(token_accumulator)
    blocks.append(block)
    write_to_pickle(block, next(block_names))

def build_block(token_stream):
    index = {}
    for token in token_stream:
        if not token[1] in index:
            index[token[1]] = [token[0]]
        else:
            index[token[1]].append(token[0])

    block: Block
    block.index = index
    block.sorted_terms = sorted(index.keys())
    return block
    # with open(block_name, 'wb') as f:
    #     pickle.dump(block, f, pickle.HIGHEST_PROTOCOL)


def block_name_generator(block_path):
    count = 1
    while True:
        yield block_path+"/block{}".format(count)
        count += 1

def write_to_pickle(block, block_name):
    with open(block_name, 'wb') as f:
        pickle.dump(block, f, pickle.HIGHEST_PROTOCOL)