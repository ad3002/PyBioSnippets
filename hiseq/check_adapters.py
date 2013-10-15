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

def check_adapters(settings):
	'''
	'''
	print "Load library"
	with open(settings["pickle_libraries_file"]) as fh:
		library = cPickle.load(fh)
	library = library[settings["k"]]
	print "Iter over kmers"
	for d in sc_read_simple_tab_file(settings["pickle_libraries_file"]):
		(kmer, tf) = d
		rkmer = get_revcomp(kmer)
		if kmer in library or rkmer in library:
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
	settings["k"] = args["k"] 
	check_adapters(settings)