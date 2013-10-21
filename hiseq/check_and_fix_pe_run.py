#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from PyBioSnippets.hiseq.fastq_tools import iter_pe_data
import argparse

def main(fastq1_file, fastq2_file):
	'''
	'''
	with open(fastq1_file+".temp", "w") as fh1:
		with open(fastq2_file+".temp", "w") as fh2:
			for i, (read1, read2) in enumerate(iter_pe_data(fastq1_file, fastq2_file)):
				print i, read1.head, read2.head
				assert read1.split()[0] == read2.split()[0]
				fh1.write(read1.fastq)
				fh2.write(read2.fastq)

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Check PE run.')
	parser.add_argument('-1','--fastq1', help='Fastq file 1', required=True)
	parser.add_argument('-2','--fastq2', help='Fastq file 2', required=True)
	args = vars(parser.parse_args())

	main(args["fastq1"], args["fastq2"])
