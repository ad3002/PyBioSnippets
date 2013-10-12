#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from trseeker.seqio.tab_file import sc_read_simple_tab_file
import pymongo
from pymongo import MongoClient
	

def kmer_to_repbase_with_mongo(kmer_file):

	client = MongoClient()
	client = MongoClient('mongodb://localhost:27017/')
	db = client.Repbase

	file_name = "/home/bioinf/htdocs/public/female.seal.log"

	index = db.MainIndex
	name_index = db.NameIndex

	name_hash = {}

	print "Iter over kmers"
	for d in sc_read_simple_tab_file(kmer_file):
		(kmer, tf) = d
		kmer = kmer.lower()
		print kmer, tf
		data = index.find_one({'kmer':kmer})
		if not data:
			rkmer = get_revcomp(kmer)
			data = index.find_one({'kmer':rkmer})
		if data:
			matches = data["index"]
			for rid, tf in matches:
				if rid in name_hash:
					name = name_hash[rid]
				else:
					name = name_index.find_one({"kid":rid})
					name = name["name"]
					name_hash[rid] = name
				print "\t", name, tf
		else:
			print "\t???"