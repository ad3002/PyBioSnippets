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

def separate_reads_witn_n_and_sharps(fastq_file, output_file, reads_with_n_file, reads_with_sharp_file):
	''' Separate reads from fastq file witn N and sharp quality scores.
	'''
	reads = []
	print "Read data..."
	k = 0
	s = 0
	with open(output_file, "w") as good_fh:
		with open(reads_with_n_file, "w") as bad_fh:
			with open(reads_with_sharp_file, "w") as sharp_fh:
				for i, read in enumerate(fastq_reader(fastq_file)):
					if "n" in read.sequence or "N" in read.sequence:
						k += 1 
						print i, k, s, float(k+1)/(i+1), float(s+1)/(i+1), "\r",
						bad_fh.write(read.fastq)
					elif "#" in read.qual:
						s += 1
						print i, k, s, float(k+1)/(i+1), float(s+1)/(i+1), "\r",
						sharp_fh.write(read.fastq)
					else:
						good_fh.write(read.fastq)
	print