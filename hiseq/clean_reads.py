#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from PyBioSnippets.hiseq.fastq_tools import separate_reads_witn_n_and_sharps

if __name__ == '__main__':
	if len(sys.argv) != 7:
		print "Usage: name.py fastq1_file fastq2_file fastq1ok_file fastq2ok_file fastq_se_file fastq_bad_file"
		exit(0)
	else:
		fastq1_file = sys.argv[1]
		fastq2_file = sys.argv[2]
		fastq1ok_file = sys.argv[3]
		fastq2ok_file = sys.argv[4]
		fastq_se_file  = sys.argv[5]
		fastq_bad_file  = sys.argv[6]
	clean_pair_reads_data(fastq1_file, fastq2_file, fastq1ok_file, fastq2ok_file, fastq_se_file, fastq_bad_file)