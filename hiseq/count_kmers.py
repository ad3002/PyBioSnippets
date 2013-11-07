#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from trseeker.tools.jellyfish import sc_count_and_dump_kmers_for_file
from PyBioSnippets.hiseq.fastq_tools import fastq_to_fasta
import argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Count')
	parser.add_argument('-p','--prefix', help='Fastq file prefix', required=True)
	parser.add_argument('-k','--ksize', help='K', required=False, default=23)
	parser.add_argument('-m','--mintf', help='mintf', required=False, default=0)
	parser.add_argument('-d','--dumpmintf', help='dumpmintf', required=False, default=100)
	args = vars(parser.parse_args())

	prefix = args["prefix"]
	k = args["ksize"]
	mintf = args["mintf"]
	dumpmintf = args["dumpmintf"]

	fastq_file = prefix + ".fastq"
	fasta_file = prefix + ".fa"
	jf_db = prefix + ".%s.jf" % k
	jf_dat  = prefix + ".%s.dat" % k

	fastq_to_fasta(fastq_file, fasta_file)

	sc_count_and_dump_kmers_for_file(fasta_file, ".", jf_db, jf_dat, k, mintf, dumpmintf)