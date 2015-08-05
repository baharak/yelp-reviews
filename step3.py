#!/bin/python

import copy
import os
import sys
import json
import math
import random
import re

from collections import namedtuple
from collections import defaultdict

Review = namedtuple('Review', ['id', 'positive', 'wordcounts'])
CLASSES = ["positive"]

smoothing = True
squareloss = False

for arg in sys.argv[1:]:
	if arg == '--nosmoothing' or arg == '-nosmoothing' or arg == '-n':
		smoothing = False;
	elif arg == '--squaredloss' or arg == '-squaredloss' or arg == '-s':
		squareloss = True;

def learn(reviews):

    m = len(reviews[0].wordcounts)

    def compute_table(reviews_c):
    	if smoothing:
    		init = 1.0
    	else:
    		init = 0.0
        table_c = [[init for i in range(m)],[init for i in range(m)]]
        for pos in 1, 0:
            for review in reviews_c[pos]:
                for index, word in enumerate(review.wordcounts):
                    table_c[pos][index] += word

            for index in range(0, m):
                table_c[pos][index] /= (len(reviews_c[pos]) + init*2)

        return table_c


    reviews_cs = [[], []] # per class classification of reviews [neg, pos]

    for review in reviews:
        pos = review.positive
        reviews_cs[pos].append(review)

    p_cs = [[], []] # p_cs[0] = p(~C), p_cs[1] = p(C)
    for pos in 1, 0:
        p_cs[pos] = 1.0 + len(reviews_cs[pos])
        p_cs[pos] /= (len(reviews) + 2)

    table_cs = compute_table(reviews_cs)

    return table_cs, p_cs



def test(reviews, table_cst, p_cst):

    loss = 0 #defaultdict(int)

    for review in reviews:
        num, den = p_cst[1], p_cst[0]
        for word, count in enumerate(review.wordcounts):
            if count:
                num *= table_cst[1][word]*2
                den *= table_cst[0][word]*2
        #print num,den
        belongs = (num > den)
        #print belongs
        if smoothing:
            p_num = num / (num+den)
            p_den = den / (num+den)
        else:
            if num + den == 0:
               p_num = p_cst[1]
               p_den = p_cst[0]
            else:
               p_num = num / (num+den)
               p_den = den / (num+den)

        belongs_real = review.positive
        if squareloss:
            if belongs_real:
                loss += (1-p_num)**2
            else:
                loss += (1-p_den)**2
        else:
            loss += (belongs ^ belongs_real)

    return loss



if __name__ == '__main__':

    f = open(sys.argv[1],'r')
    all_reviews = [] # dictionary of reviews by their id
    counter = 0
    for line in f:
        line = line.strip()
        if len(line) == 0 :
            continue;
        counter += 1
        line_list = line.split(",") # strip whitespace from begin/end
        all_reviews.append(Review( id = counter,
                            positive = (line_list[0] == '1'),
                            wordcounts = map(int,line_list[1:])    ) )

resultdic_ls = {}
resultdic_std = {}

size = len(all_reviews)/10 # or 10 if sample data

ord = random.sample(range(size*10), size*10)
print 'TSS\tLOSS\tSTD'
for tss2 in range(1,10): #CHANGE IT TO 9
    resultdic = [0.0 for i in range(10)]
    tss = tss2 * size
    resultdic[tss2]=[]
    resultdic_ls[tss2]= []
    for i in range(0,10):
        test_set = []
        data = []
        start = i * size
        for j in range(start,start+size):
        	test_set.append(all_reviews[ord[j]])
        for j in range(0, start):
        	data.append(all_reviews[ord[j]])
        for j in range(start+size, size*10):
        	data.append(all_reviews[ord[j]])

        learn_set = []
        ind = random.sample(range(9), tss2)
        for j in range(tss2):
        	for k in range(size):
        		learn_set.append(data[ind[j]*size+k])
        table_cs, p_cs  = learn(learn_set)

        loss  = test(test_set, table_cs, p_cs)

        resultdic[i]=(float(loss) /size)  #, float(square_loss) /size)) # mismatch / numberof testsize=10

    avg = 0
    for i in range(10):
    	avg += resultdic[i] / 10.0
    std = 0
    for i in range(10):
    	std += (resultdic[i]-avg)**2
    std = math.sqrt(std/10.0)
    print tss, '\t',avg, '\t', std
