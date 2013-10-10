#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from trseeker.seqio.sra_file import fastq_reader

def fix_uncorrect_long_quality(fastq_file, corrected_fastq_output):
	''' Fix too long quality scores in corrupted HiSeq files
	'''
	bp200 = 0
	total = 0.
	with open(corrected_fastq_output, "w") as fh:
		for i, read in enumerate(fastq_reader(fastq_file)):
			print i, "\r",
			if len(read.seq) != len(read.qual):
				read.qual = read.qual[:len(read.seq)]
				print
				print read.fastq
			fh.write(read.fastq)