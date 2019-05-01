#!/usr/bin/env python3

import sys
import csv
import os
import collections

ARGUMENTS = sys.argv[1:]
FILENAME = 'word_lists.csv'
LIST_ALL = False
PREFIX = ''
CONTAINS = ''
MEANING = ''
POS = ''
POS_DIR = {'wr'  : 'Word Root',
           'suf' : 'Suffix',
           'pre' : 'Prefix',
           'ba'  : 'Body Axis',
           'pos' : 'Position' }
PARSE = False

class Word(object):
    def __init__(self, word):
        self.term = word[0].replace("-", "").replace(" ", "")
        self.definition = word[1]
        self.greek_latin = word[2]
        self.pos = word[3]

class Node(object):
    def __init__(self, word):
        self.word = word
        self.children = []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.word.term)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

class Tree(object):
    def __init__(self, root):
        self.root = root 

def usage(exit_code=0):
    print('''Usage: {} [-f filename -p PREFIX -l]
    -f     FILENAME Load in words from file (Default: \'word_lists.csv\')
    -p     PREFIX   Get all words beginning with prefix
    -c     CONTAINS Get words containing substring (to be: word matching)
    -m     MEANING  Get words that contain MEANING in their definition
    -pos   POS      Narrow down list by part of speech (wr, suf, pre, ba, pos)
    -parse TERM     Find all word roots in a term'''.format(os.path.basename(sys.argv[0])))
    sys.exit(exit_code)


def load_words():
    word_list = []

    with open(FILENAME, newline='') as csvfile:
        wlreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(wlreader):
            if index: # ignore first line with template
                word_list.append(Word(row))

    return word_list

def list_all(word_list):
    for i, w in enumerate(word_list):
        print("Term {}: {}\nDefinition: {}\nGreek/Latin: {}\nPOS: {}\n\n".format(i + 1, w.term, w.definition, w.greek_latin, w.pos))

    print("Grace 'G$' Milton's Project for CLAS 30330")

def prefix(word_list):
    new_word_list = []

    for word in word_list:
        if word.term.lower().startswith(PREFIX.lower()):
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def contains(word_list):
    new_word_list = []

    for word in word_list:
        if CONTAINS.lower() in word.term.lower():
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def meaning(word_list):
    new_word_list = []

    for word in word_list:
        if MEANING.lower() in word.definition.lower():
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def pos(word_list):
    new_word_list = []

    for word in word_list:
        if word.pos == POS:
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def list_pos(word_list):
    pos_set = set()

    for word in word_list:
        pos_set.add(word.pos)

    for pos in pos_set:
        print(pos)

def find_all_wr(word_list, term):
    wr_start_dict = collections.defaultdict(list)
    word_roots = []

    for word in word_list:
        if word.term.lower() in term:
            i = term.find(word.term.lower())
            wr_start_dict[i].append(word)
            word_roots.append(word)

    return wr_start_dict, word_roots
    
def combine_wrs(wr_dict, wr_list, term):
    possible_parses = []
    i = list(sorted(wr_dict.keys()))[0]
    for wr in wr_dict[i]:
        node = Node(wr)
        possible_parses.append(Tree(node))
    for branch in possible_parses:
        j = i
        node = branch.root
        frontier = [[node, j]]
        while frontier:
            node, j = frontier.pop(0)
            k = j + len(node.word.term)
            j = find_next_wr(wr_dict, term, k)
            while j and j < len(term):
                for wr in wr_dict[j]:
                    child = Node(wr)
                    node.children.append(child)
                    frontier.append([child, j])
                j += 1
    for p in possible_parses:
        print(p.root)
    return possible_parses

def find_next_wr(wr_dict, term, i):
    while i not in wr_dict and i < len(term):
        i += 1
    if i >= len(term):
        return None
    return i
    
     
        

if __name__ == "__main__":

    while ARGUMENTS and ARGUMENTS[0].startswith('-') and len(ARGUMENTS[0]) > 1:
        arg = ARGUMENTS.pop(0)
        if arg == '-f':
            FILENAME = ARGUMENTS.pop(0)
            LIST_ALL = True
        elif arg == '-p':
            PREFIX = ARGUMENTS.pop(0)
            LIST_ALL = True
        elif arg == '-c':
            CONTAINS = ARGUMENTS.pop(0)
            LIST_ALL = True
        elif arg == '-m':
            MEANING = ARGUMENTS.pop(0)
            LIST_ALL = True
        elif arg == '-pos':
            POS = ARGUMENTS.pop(0)
            if POS in POS_DIR:
                POS = POS_DIR[POS]
            else:
                POS = ''
            LIST_ALL = True
        elif arg == '-parse':
            PARSE = True
            term = ARGUMENTS.pop(0)
        elif arg == '-h':
            usage(0)
        else:
            usage(1)

    word_list = load_words()
 
    if PREFIX:
        word_list = prefix(word_list)
    if CONTAINS:
        word_list = contains(word_list)
    if MEANING:
        word_list = meaning(word_list)
    if POS:
        word_list = pos(word_list)
    if PARSE:
        wr_dict, wr_list = find_all_wr(word_list, term)
        print("TERM: {}".format(term))
        for wr in wr_list:
            print("    {} - {}".format(wr.term, wr.definition))
        print("\n")
        possible_parses = combine_wrs(wr_dict, wr_list, term)

    if LIST_ALL:
        list_all(word_list)
