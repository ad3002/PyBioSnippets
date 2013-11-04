#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from PyBioSnippets.hiseq.fastq_tools import clean_single_read_data
import argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Check presence of adapter kmers.')
	parser.add_argument('-p','--prefix', help='SE prefix', required=True)
	parser.add_argument('-v','--verbose', help='Verbose', required=False, default=False)
	parser.add_argument('-G','--polyG', help='Length of polyG', required=False, default=23)
	parser.add_argument('-c','--cutoff', help='Length cutoff', required=False, default=50)
	parser.add_argument('-a','--adapters', help='File with adapters', required=False, default=None)
	args = vars(parser.parse_args())

	prefix = args["prefix"]
	verbose = args["verbose"]
	cutoff = int(args["cutoff"])
	polyG_cutoff = int(args["polyG"])
	adapters_file = args["adapters"]
	fastq1_file = "%s.fastq" % prefix
	fastq1ok_file = "%s.ok.fastq" % prefix
	fastq_bad_file  = "%s.bad.fastq" % prefix
	clean_single_read_data(fastq1_file, fastq1ok_file, fastq_bad_file, verbose=verbose, adapters_file=adapters_file, cutoff=cutoff, polyG_cutoff=polyG_cutoff)