#!/bin/python

import copy
import os
import sys
import json
import math
import random
import re
import csv

from collections import namedtuple
from collections import defaultdict


def parse_words(text):
    return text.split()#map(lambda s: s.lower(), re.findall(r'\b[a-z]+\b', text, re.I))



def create_wordbag(review, most_freq):
    wordbag = defaultdict(int)
    for word in most_freq:
        wordbag[word] = 0
    for word in review:
        if word in most_freq:
            wordbag[word] = 1
    return wordbag

def reading_reviews():

    with open('reviews.csv', 'rb') as csvreading:
        l = []
        reader = csv.reader(csvreading,  delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            rev_text = row[1].replace('\\n','\n')
            words = parse_words(rev_text)
            assert type(words) == type([])
            l.append((int(row[0]),words))

        return l



if __name__ == '__main__':

    f = open(sys.argv[1],'r')
    wordbag = (defaultdict(int), defaultdict(int))

    for positive, words in reading_reviews():
        for word in words:
            wordbag[0][word] += 1
        for word1, word2 in zip(words[:-1], words[1:]):
            wordbag[1][word1, word2] += 1


    if sys.argv[2] == '-u':
	    uni = True
    elif sys.argv[2] == '-b' :
	    uni = False

    if uni:
        N1 = 5000 ## change them to 5000 and 2500
        N2 = 0
    else:
        N1 = 2500
        N2 = 2500

    for word in sorted(wordbag[0], key=wordbag[0].get, reverse=True)[N1:]:
        wordbag[0].pop(word)


    for word in sorted(wordbag[1], key=wordbag[1].get, reverse=True)[N2:]:
        wordbag[1].pop(word)


    wordbag_all = {}
    wordbag_all.update(wordbag[0])
    wordbag_all.update(wordbag[1])

    outputname = sys.argv[2] +"data" + ".csv"
    with open(outputname, 'wb') as csvwriting:
        datawriter = csv.writer(csvwriting , delimiter=',', quoting=csv.QUOTE_NONE)
        for positive, words in reading_reviews():
           wordbag_r = create_wordbag(words, wordbag_all)
           vv =[ wordbag_r[word] for word in sorted(wordbag_r.keys()) ]
           datawriter.writerow([int(positive)] + vv )
