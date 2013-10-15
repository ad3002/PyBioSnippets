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
	print "Iter over kmers"
	for i, d in enumerate(sc_read_simple_tab_file(settings["fastq_file"])):
		(kmer, tf) = d
		kmer = kmer.lower()
		print i, kmer, tf, "\r",
		rkmer = get_revcomp(kmer)
		if kmer in library or rkmer in library:
			print
			print kmer, tf, library[kmer]

if __name__ == '__main__':
	
	settings = {
		"pickle_libraries_file": "/home/akomissarov/libs/illumina.pickle",
	}

	parser = argparse.ArgumentParser(description='Check presence of adapter kmers.')
	parser.add_argument('-i','--input', help='Input jellyfish dat file', required=True)
	parser.add_argument('-k','--k', help='K for kmers', required=False, default=23)
	args = vars(parser.parse_args())
	settings["fastq_file"] = args["input"] 
	settings["k"] = int(args["k"])
	check_adapters(settings)