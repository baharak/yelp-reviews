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


Review = namedtuple('Review', [ 'positive', 'rev_text'])



def is_rating_positive(obj):
    if "stars" not in obj:
        return False
    return obj["stars"] > 3.5
    
    
if __name__ == '__main__':
    f = open(sys.argv[1],'r')
    all_reviews = [] # dictionary of reviews by their id
    for line in f:
        line = line.strip() # strip whitespace from begin/end
        if len(line) == 0:
            continue
        obj = json.loads(line)
        if obj["type"] == 'review':
            if "votes" in obj:
                votes = obj["votes"]
                if 3 <= sum(votes.values()) <= 10:
                    if "text" in obj:
                        all_reviews.append(Review(
                                positive=is_rating_positive(obj),
                                rev_text=obj["text"] ) )
    
    
    with open('reviews.csv', 'wb') as csvwriting:    
        spamwriter = csv.writer(csvwriting , delimiter=',', quoting=csv.QUOTE_ALL)    
        for review in all_reviews:
            spamwriter.writerow([int(review.positive) , unicode( review.rev_text.replace('\n','\\n') ).encode("utf-8") ])    
