#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from PyBioSnippets.hiseq.fastq_tools import clean_short_reads
import argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Romove short reads from fastq.')
	parser.add_argument('-p','--prefix', help='SE prefix', required=True)
	parser.add_argument('-v','--verbose', help='Verbose', required=False, default=False)
	parser.add_argument('-c','--cutoff', help='Cutoff', required=True)
	args = vars(parser.parse_args())

	prefix = args["prefix"]
	verbose = args["verbose"]
	cutoff = args["cutoff"]
	fastq1_file = "%s.fastq" % prefix
	fastq1ok_file = "%s.ok.fastq" % prefix
	fastq_short_file  = "%s.short.fastq" % prefix
	clean_short_reads(fastq1_file, fastq1ok_file, fastq_short_file, cutoff, verbose=verbose)