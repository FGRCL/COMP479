import argparse
from ir.p3.data.spimi_block import Block
from ir.p3.util import write_to_pickle
from ir.p3.external_merge import build_final_index
from ir.p3.data.posting import Posting
from ir.p2 import stream_filters
from ir.p1 import solutions


def build_index(in_path, out_path):
    spimi_invert(
        parse_document(in_path),
        500,
        out_path
    )


def spimi_invert(token_stream, max_dictionary_size, block_path):
    count = 0
    token_accumulator = []
    block_names = block_name_generator(block_path)
    for token in token_stream:
        count += 1
        token_accumulator.append(token)
        if count == max_dictionary_size:
            block_name = next(block_names)
            block = build_block(token_accumulator, block_name[1])
            write_to_pickle(block, block_name[0])
            count = 0
            token_accumulator = []

    block_name = next(block_names)
    block: Block = build_block(token_accumulator, block_name[1])
    write_to_pickle(block, block_name[0])

    build_final_index(block_path)


def parse_document(in_path):
    return stream_filters.tokenizer(
        solutions.block_extractor(
            solutions.block_document_segmenter(
                solutions.block_reader(in_path)
            )
        )
    )


# TODO sort the postings list?
def build_block(token_stream, count):
    index = {}
    for token in token_stream:
        if not token[1] in index:
            posting = Posting(token[0], 1)
            index[token[1]] = [posting]
        else:
            posting = next(filter(lambda posting: posting.doc_id == token[0], index[token[1]]), None)
            if posting is not None:
                posting.term_count += 1
            else:
                posting = Posting(token[0], 1)
                index[token[1]].append(posting)

    for term in index:
        index[term].sort(key=lambda posting: posting.doc_id)
    block: Block = Block(index, sorted(index.keys()), count)
    return block


def block_name_generator(block_path):
    count = 1
    while True:
        yield (block_path+"/block{}.pickle".format(count), count)
        count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Reuters')
    parser.add_argument('-p', '--path', help='Reuters collection directory')
    parser.add_argument('-i', '--index', help="The index outputfile")
    args = parser.parse_args()

    build_index(args.path, args.index)