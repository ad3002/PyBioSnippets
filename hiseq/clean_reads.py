#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from PyBioSnippets.hiseq.fastq_tools import clean_pair_reads_data
import argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Check presence of adapter kmers.')
	parser.add_argument('-p','--prefix', help='Pair prefix', required=True)
	parser.add_argument('-v','--verbose', help='Verbose', required=False, default=False)
	parser.add_argument('-a','--adapters', help='File with adapters', required=False, default=None)
	parser.add_argument('-c','--cutoff', help='Cutoff length', required=False, default=50)
	args = vars(parser.parse_args())

	prefix = args["prefix"]
	verbose = args["verbose"]
	cutoff = args["cutoff"]
	adapters_file = args["adapters"]
	fastq1_file = "%s1.fastq" % prefix
	fastq2_file = "%s2.fastq" % prefix
	fastq1ok_file = "%s1.ok.fastq" % prefix
	fastq2ok_file = "%s2.ok.fastq" % prefix
	fastq_se_file  = "%s.se.fastq" % prefix
	fastq_bad_file  = "%s.bad.fastq" % prefix
	clean_pair_reads_data(fastq1_file, fastq2_file, fastq1ok_file, fastq2ok_file, fastq_se_file, fastq_bad_file, verbose=verbose, adapters_file=adapters_file, cutoff=cutoff)