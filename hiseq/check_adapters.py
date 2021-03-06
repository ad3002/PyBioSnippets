#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
'''
'''

import os
import sys
import re
from collections import defaultdict
import argparse
import cPickle
from trseeker.tools.sequence_tools import get_revcomp
from trseeker.seqio.tab_file import sc_read_simple_tab_file

def check_adapters(settings):
	'''
	'''
	print "Load library for key=", settings["k"]
	with open(settings["pickle_libraries_file"]) as fh:
		library = cPickle.load(fh)
	library = library[settings["k"]]
	assert len(library.keys()[0]) == settings["k"]
	print "Library size:", len(library.keys())
	contaminated_kmers = {}
	print "Iter over kmers"
	for i, d in enumerate(sc_read_simple_tab_file(settings["fastq_file"])):
		(kmer, tf) = d
		tf = int(tf)
		kmer = kmer.lower()
		print i, kmer, tf, "\r",
		if settings["cutoff"] and tf < settings["cutoff"]:
			break
		rkmer = get_revcomp(kmer)
		if kmer in library or rkmer in library:
			print
			print kmer, tf, library[kmer]
			contaminated_kmers[kmer] = (tf, library[kmer])
	all_kmers = set(contaminated_kmers.keys())
	contaminated_kmers = contaminated_kmers.items()
	contaminated_kmers.sort(key=lambda x: x[1], reverse=True)
	print "Save data"
	with open(settings["output_file"], "w") as fh:
		for (k, v) in contaminated_kmers:
			rkey = get_revcomp(k)
			s = "%s\t%s\n" % (k, v)
			fh.write(s)
			if not rkey in all_kmers:
				s = "%s\t%s\n" % (rkey, v)
				fh.write(s)
	return contaminated_kmers

if __name__ == '__main__':
	
	settings = {
		"pickle_libraries_file": "/home/akomissarov/Dropbox/PyBioSnippets/hiseq/illumina.pickle",
	}

	parser = argparse.ArgumentParser(description='Check presence of adapter kmers.')
	parser.add_argument('-i','--input', help='Input jellyfish dat file', required=True)
	parser.add_argument('-o','--output', help='Output dat file', required=True)
	parser.add_argument('-k','--k', help='K for kmers', required=False, default=23, type=int)
	parser.add_argument('-c','--cutoff', help='Maximal tf', required=False, default=None, type=int)

	args = vars(parser.parse_args())
	settings["fastq_file"] = args["input"] 
	settings["output_file"] = args["output"]
	settings["cutoff"] = args["cutoff"]
	settings["k"] = int(args["k"])
	check_adapters(settings)