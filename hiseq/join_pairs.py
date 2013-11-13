#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from trseeker.seqio.sra_file import fastq_reader
import argparse

def get_next_pair(fh1, fh2, fse):
	"""
	"""
	try:
		read1 = fh1.next()
	except:
		for read2 in fh2:
			fse.write(read2.fastq)
		return None, None
	try:
		read2 = fh2.next()
	except:	
		for read1 in fh1:
			fse.write(read1.fastq)
		return None, None
	while True:
		if read1.read_id < read2.read_id:
			while read1.read_id < read2.read_id:
				fse.write(read1.fastq)
	 			try:
					read1 = fh1.next()
				except:
					for read2 in fh2:
						fse.write(read2.fastq)
					return None, None
		if read2.read_id < read1.read_id:
			while read2.read_id < read1.read_id:
				fse.write(read2.fastq)
				try:
					read2 = fh2.next()
				except:
					for read1 in fh1:
						fse.write(read1.fastq)
					return None, None
		if read2.read_id == read1.read_id:
			return read1, read2

def main(fastq1_file, fastq2_file, fastq1ok_file, fastq2ok_file, fastq_se_file):
	"""
	"""
	fh1 = fastq_reader(fastq1_file)
	fh2 = fastq_reader(fastq2_file)

	wh1 = open(fastq1ok_file, "w")
	wh2 = open(fastq2ok_file, "w")
	fse = open(fastq_se_file, "w")

	i = 0

	while True:
		read1, read2 = get_next_pair(fh1, fh2, fse)
		if read1 is None:
			break
		wh1.write(read1.fastq)
		wh2.write(read2.fastq)
		i += 1
		print i, "\r",
	print

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Drop single reads.')
	parser.add_argument('-p','--prefix', help='prefix', required=True)
	args = vars(parser.parse_args())

	prefix = args["prefix"]

	fastq1_file = "%s_1.ok.fastq" % prefix
	fastq2_file = "%s_2.ok.fastq" % prefix
	fastq1ok_file = "%s_1.done.fastq" % prefix
	fastq2ok_file = "%s_2.done.fastq" % prefix
	fastq_se_file  = "%s.se.fastq" % prefix
	main(fastq1_file, fastq2_file, fastq1ok_file, fastq2ok_file, fastq_se_file)