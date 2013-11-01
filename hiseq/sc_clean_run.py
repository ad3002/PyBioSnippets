#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
'''
'''
import sys
sys.path.append("/home/akomissarov/Dropbox")

import os
import re
from collections import defaultdict
import argparse
import cPickle
from trseeker.tools.sequence_tools import get_revcomp
from PyBioSnippets.hiseq.fastq_tools import clean_single_read_data


def clean_se_run(settings):
	'''
	'''
	# 1. Reads filter illumina kmers
	# 2. Filter data
	# 3. Save
	print "Load library for key=", settings["k"]
	with open(settings["pickle_libraries_file"]) as fh:
		library = cPickle.load(fh)
	library = library[settings["k"]]
	kmers =set(library.keys())
	for kmer in library.keys():
		kmers.add(get_revcomp(kmer))
	with open(settings["dat_libraries_file"], "w") as fh:
		for kmer in kmers:
			fh.write("%s\t-\n" % kmer)

	prefix = settings["prefix"]
	verbose = settings["verbose"]
	adapters_file = settings["dat_libraries_file"]
	fastq1_file = "%s.fastq" % prefix
	fastq1ok_file = "%s.ok.fastq" % prefix
	fastq_bad_file  = "%s.bad.fastq" % prefix
	clean_single_read_data(fastq1_file, fastq1ok_file, fastq_bad_file, verbose=verbose, adapters_file=adapters_file,
			cutoff=settings["cutoff"], polyG_cutoff=settings["polyGcutoff"]
		)


if __name__ == '__main__':
	
	settings = {
		"pickle_libraries_file": "/home/akomissarov/Dropbox/PyBioSnippets/hiseq/illumina.pickle",
		"dat_libraries_file": "/home/akomissarov/Dropbox/PyBioSnippets/hiseq/illumina.dat",
	}

	parser = argparse.ArgumentParser(description='Clean single run.')
	parser.add_argument('-i','--input_prefix', help='Input fastq file prefix without .fastq', required=True)
	parser.add_argument('-k','--ksize', help='Value of k', required=False, default=23)
	parser.add_argument('-v','--verbose', help='Verbose', required=False, default=True)
	parser.add_argument('-c','--cutoff', help='Cutoff', required=False, default=50)
	parser.add_argument('-g','--polyGcutoff', help='PolyG/C length cutoff', required=False, default=13)
	
	args = vars(parser.parse_args())
	settings["prefix"] = args["input_prefix"] 
	settings["verbose"] = args["verbose"]
	settings["k"] = args["ksize"]
	settings["cutoff"] = args["cutoff"]
	settings["polyGcutoff"] = args["polyGcutoff"]
	clean_se_run(settings)