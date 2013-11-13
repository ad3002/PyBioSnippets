#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from trseeker.tools.edit_distance import hamming_distance
import argparse

def main(kmer, db_file, hd):
	'''
	'''

	with open(db_file) as fh:
		db_kmers = fh.readlines()
	db_kmers_q = [x.strip().split()[0].lower() for x in db_kmers]
	result = set([kmer,])
	for i, db_kmer in enumerate(db_kmers_q):
		if hamming_distance(db_kmer, kmer) <= hd:
			print db_kmers[i]
			result.add(db_kmer)
	return result

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Get list of kmers over hamming distance.')
	parser.add_argument('-i','--kmer', help='Input kmer', required=True)
	parser.add_argument('-d','--db', help='List of database kmers', required=True)
	parser.add_argument('-e','--hamming', help='Hammming distance', required=True)
	args = vars(parser.parse_args())

	kmer = args["kmer"].lower()
	db_file = args["db"]
	hd = int(args["hamming"])
	main(kmer, db_file, hd)