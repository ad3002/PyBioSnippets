#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from trseeker.seqio.tab_file import sc_iter_simple_tab_file
from trseeker.tools.sequence_tools import get_revcomp
import pymongo
from pymongo import MongoClient
import sys
from collections import defaultdict

def kmer_to_cegma_with_mongo(kmer_file, verbose=False):

	client = MongoClient()
	client = MongoClient('mongodb://localhost:27017/')
	db = client.Repbase

	index = db.CegmaMainIndex
	name_index = db.CegmaNameIndex
	repbase_index = db.MainIndex

	name_hash = {}

	print "Iter over kmers"
	match = {
		"repbase": 0,
		"cegma": 0,
		"repbase_cegma": 0,
		"other": 0,
	}
	match_distr = {
		"repbase": defaultdict(int),
		"cegma": defaultdict(int),
		"repbase_cegma": defaultdict(int),
		"other": defaultdict(int),
	}
	for d in sc_iter_simple_tab_file(kmer_file):
		
		(kmer, tf) = d
		repbase_hit = False
		cegma_hit = False
		# print tf, kmer, "\r",
		tf = int(tf)
		print match, tf, "\r", 
		kmer = kmer.lower()
		# if verbose:
		# 	print tf, kmer, "\r",
		data = repbase_index.find_one({'kmer':kmer})
		if not data:
			rkmer = get_revcomp(kmer)
			data = repbase_index.find_one({'kmer':rkmer})
		if data:
			repbase_hit = True

		data = index.find_one({'kmer':kmer})
		if not data:
			rkmer = get_revcomp(kmer)
			data = index.find_one({'kmer':rkmer})
		if data:
			matches = data["index"]
			cegma_hit = True
		# 	print
		# 	print kmer, tf
		# 	for rid, tf in matches:
		# 		if rid in name_hash:
		# 			name = name_hash[rid]
		# 		else:
		# 			name = name_index.find_one({"kid":rid})
		# 			name = name["name"].strip()
		# 			name_hash[rid] = name
		# 		print "\t", name, tf
		# else:
		# 	# print "\t???"
		# 	pass
		if repbase_hit and cegma_hit:
			match["repbase_cegma"] += 1
			match_distr["repbase_cegma"][tf] += 1
			continue
		elif repbase_hit:
			match["repbase"] += 1
			match_distr["repbase"][tf] += 1
			continue
		elif cegma_hit:
			match["cegma"] += 1
			match_distr["cegma"][tf] += 1
			continue
		else:
			match["other"] += 1
	print
	print match_distr
	print match

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: program_name.py kmer_file > annotation_file.txt"
		exit(0)
	kmer_file = sys.argv[1]
	verbose = True
	kmer_to_cegma_with_mongo(kmer_file, verbose=verbose)