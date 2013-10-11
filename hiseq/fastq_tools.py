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

def is_bad_read(sequence, qual):
	''' Check read quality.
	1. Presence of unknown nucelotides.
	2. Presence of 0 quality nucelotides.
	3. Presence of polyC tracks.
	4. Presence of polyC tracks.
	'''
	if "n" in sequence:
		return "N"
	if "#" in qual:
		return "zero_qual"
	if "ccccccccccccccccccccccc" in sequence:
		return "polyC"
	if "ggggggggggggggggggggggg" in sequence:
		return "polyG"
	return None

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

def filter_reads_by_gc(fastq_file, output_file, min_gc, max_gc):
	''' Filter reads between min_gc and max_gc.
	'''
	with open(output_file, "w") as fh:
		for read in fastq_reader(fastq_file):
			gc = read.gc
			if gc < max_gc and gc > min_gc:
				print round(gc, 3), read.seq
				fh.write(read.fasta)