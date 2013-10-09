#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from collections import defaultdict

def compute_histogram(data_tab_file):
	'''
	'''
	D = defaultdict(int)
	with open(data_tab_file) as fh:
		for line in fh:
			data = line.strip().split("\t")
			D[int(data[1])] += 1
	return D

def compute_kmers_freq(D, output_file):
	'''
	'''
	total = 0.0
	for x, y in lines:
	    D[y] += x
	    total += x
	D = D.items()
	D.sort()
	with open(output_file, "w") as fh:
	    for k, v in D:
	        s = "%s\t%s\n" % (k, round(100*v/total, 3))
	        fh.write(s)

def main(input_file, output_file):
	'''
	'''
	D = compute_histogram(input_file)
	compute_kmers_freq(D, output_file)


	