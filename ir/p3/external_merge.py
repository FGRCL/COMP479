import os
from os import path
from pathlib import Path
from typing import List
from ir.p3.data.spimi_block import Block
from ir.p3.util import write_to_pickle, load_block_from_pickle
from ir.p3.data.posting import Posting


def build_final_index(path_string: str):
    merge_pass_directory_template = path_string+"/pass{}";
    pass_count = 1
    in_path = Path(path_string)
    out_path = Path(merge_pass_directory_template.format(pass_count))
    while(get_number_of_files_in_directory(in_path)>1):
        merge_blocks_in_directory(in_path, out_path)
        pass_count += 1
        in_path = out_path
        out_path = Path(merge_pass_directory_template.format(pass_count))

    final_index = load_block_from_pickle(get_files_in_directory(in_path)[0])
    write_to_pickle(final_index, path_string+"/final_index.pickle")


def merge_blocks_in_directory(in_path: path, out_path: path):
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    block_pairs = []
    files = get_files_in_directory(in_path)
    for i in range(1, len(files), 2):
        first_block = load_block_from_pickle(files[i-1])
        second_block = load_block_from_pickle(files[i])
        block_pairs.append((first_block, second_block))

    for pair in block_pairs:
        merge(pair[0], pair[1], out_path)

    if get_number_of_files_in_directory(in_path)%2 == 1:
        odd_block = load_block_from_pickle(files[len(files)-1])
        odd_block_path = "{}/{}.pickle".format(out_path, odd_block.name)
        write_to_pickle(odd_block, odd_block_path)


def merge(first_block: Block, second_block: Block, out_path: path):
    new_terms = []
    new_index = {}
    i, j = 0, 0
    while i < len(first_block.sorted_terms) and j < len(second_block.sorted_terms):
        first_term = first_block.sorted_terms[i]
        second_term = second_block.sorted_terms[j]
        if first_term < second_term:
            new_terms.append(first_term)
            new_index[first_term] = first_block.index[first_term]
            i += 1
        elif first_term > second_term:
            new_terms.append(second_term)
            new_index[second_term] = second_block.index[second_term]
            j += 1
        elif first_term == second_term:
            new_terms.append(first_term)
            merged_postings = merge_postings_list(first_block.index[first_term], second_block.index[second_term])
            new_index[first_term] = merged_postings
            i += 1
            j += 1

    while i < len(first_block.sorted_terms):
        first_term = first_block.sorted_terms[i]
        new_terms.append(first_term)
        new_index[first_term] = first_block.index[first_term]
        i += 1

    while j < len(second_block.sorted_terms):
        new_terms.append(second_term)
        new_index[second_term] = second_block.index[second_term]
        j += 1

    new_block = Block(new_index, new_terms, first_block.name + second_block.name)
    block_path = "{}/{}.pickle".format(out_path, str(first_block.name) + str(second_block.name))
    write_to_pickle(new_block, block_path)


def merge_postings_list(first_list: List[Posting], second_list: List[Posting]):
    merged_postings_list = []
    i, j = 0, 0
    while i < len(first_list) and j < len(second_list):
        first_elem = first_list[i]
        second_elem = second_list[j]
        if first_elem.doc_id < second_elem.doc_id:
            merged_postings_list.append(first_elem)
            i += 1
        if first_elem.doc_id > second_elem.doc_id:
            merged_postings_list.append(second_elem)
            j += 1
        if first_elem.doc_id == second_elem.doc_id:
            merged_posting: Posting = Posting(first_elem.doc_id, first_elem.term_count + second_elem.term_count)
            merged_postings_list.append(merged_posting)
            i += 1
            j += 1

    while i < len(first_list):
        merged_postings_list.append(first_list[i])
        i += 1

    while j < len(second_list):
        merged_postings_list.append(second_list[j])
        j += 1

    return merged_postings_list


def get_number_of_files_in_directory(path):
    full_path = get_merged_path(path)
    return len([name for name in os.listdir(full_path) if os.path.isfile(full_path+"/"+name) ])


def get_files_in_directory(path):
    full_path = get_merged_path(path)
    return [full_path+"/"+name for name in os.listdir(full_path) if os.path.isfile(full_path+"/"+name)]


def get_merged_path(path):
    return '/'.join(path.parts)