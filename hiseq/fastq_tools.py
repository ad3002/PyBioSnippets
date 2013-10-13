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

def is_bad_read(read):
	''' Check read quality.
	1. Presence of unknown nucelotides.
	2. Presence of 0 quality nucelotides.
	3. Presence of polyC tracks.
	4. Presence of polyG tracks.
	'''
	if "n" in read.sequence:
		return "N"
	if "#" in read.qual:
		return "zeroQ"
	if "ccccccccccccccccccccccc" in read.sequence:
		return "polyC"
	if "ggggggggggggggggggggggg" in read.sequence:
		return "polyG"
	return None

def clean_pair_reads_data(fastq1_file, fastq2_file, fastq1ok_file, fastq2ok_file, fastq_se_file, fastq_bad_file, verbose=False):
	''' Remove reads containing N, # quality, polyG/polyC tracks.
	'''
	wh1 = open(fastq1ok_file, "w")
	wh2 = open(fastq2ok_file, "w")
	se = open(fastq_se_file, "w")
	bad = open(fastq_bad_file, "w")

	reader1 = fastq_reader(fastq1_file)
	reader2 = fastq_reader(fastq2_file)

	statistics = {
		"pe": 0,
		"se": 0,
		"N": 0,
		"zeroQ": 0,
		"polyC": 0,
		"polyG": 0,
	}

	i = 0.
	while True:
		try:
			read1 = next(reader1)
		except StopIteration:
			try:
				read2 = next(reader2)
			except StopIteration:
				break
				pass
			raise Exception("Not equal number of reads in runs") 
			break
		read2 = next(reader2)
		i += 1
		if verbose:
			print i, statistics["pe"]/i, statistics, "\r",
		error1 = is_bad_read(read1)
		error2 = is_bad_read(read2)
		if not error1 and not error2:
			wh1.write(read1.fastq)
			wh2.write(read2.fastq)
			statistics["pe"] += 1
			continue
		if error1:
			bad.write(read1.fastq_with_error(error1))
			statistics[error1] += 1
		else:
			se.write(read1.fastq)
			statistics["se"] += 1
		if error2:
			bad.write(read2.fastq_with_error(error2))
			statistics[error2] += 1
		else:
			se.write(read2.fastq)
			statistics["se"] += 1
			
	wh1.close()
	wh2.close()
	se.close()
	bad.close()
	print
	print statistics
	return statistics


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


def split_large_fastq_file(file_name, output_file_pattern, cutoff=1000000):
	''' Split large fastq file.
	For example:
		output_file_pattern = "/home/akomissarov/data/asian_seabass/raw_reads/500bp_insert_lane1_read1.chunk%s.fastq"	
	'''

	def write_data(reads, chunk, output_file_pattern):
		with open(output_file_pattern % chunk, "w") as fh:
			for read in reads:
				fh.write(read.fastq)

	reads = []
	chunk = 1
	print "Read data..."
	for i, read in enumerate(fastq_reader(file_name)):
		print i, "\r",
		if reads and i % cutoff == 0:
			print "\nSave reads", i, "for chunk", chunk
			write_data(reads, chunk, output_file_pattern)
			chunk += 1
			reads = []
		reads.append(read)
	if reads:
		print "\nLast one. Save reads", i, "for chunk", chunk
		write_data(reads, chunk, output_file_pattern)