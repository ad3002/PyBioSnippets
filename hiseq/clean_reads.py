#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from PyBioSnippets.hiseq.fastq_tools import clean_pair_reads_data

if __name__ == '__main__':
	if len(sys.argv) not in [3, 2, 4]:
		print "Usage: name.py pair_prefix [verbose]"
		exit(0)
	verbose = False
	if len(sys.argv) == 3:
		verbose = True
	prefix = sys.argv[1]
	fastq1_file = "%s1.fastq" % prefix
	fastq2_file = "%s2.fastq" % prefix
	fastq1ok_file = "%s1.ok.fastq" % prefix
	fastq2ok_file = "%s2.ok.fastq" % prefix
	fastq_se_file  = "%s.se.fastq" % prefix
	fastq_bad_file  = "%s.bad.fastq" % prefix
	clean_pair_reads_data(fastq1_file, fastq2_file, fastq1ok_file, fastq2ok_file, fastq_se_file, fastq_bad_file, verbose=verbose)