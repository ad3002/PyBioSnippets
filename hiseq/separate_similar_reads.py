#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import os
import sys
import re
from collections import defaultdict
import argparse
import cPickle
from trseeker.tools.sequence_tools import get_revcomp
from trseeker.seqio.tab_file import sc_read_simple_tab_file
from trseeker.tools.ngrams_tools import get_for_and_rev_kmers_from_fastq

def filter_reads_by_fasta(settings):
	'''
	'''
	path_to_script = "/home/akomissarov/libs/rm_reads/rm_reads"
	fasta_file = settings["fasta_file"]
	index_file = settings["fasta_file"] + ".kmers"
	k = settings["k"]
	library = get_for_and_rev_kmers_from_fastq(fasta_file, k)
	with open(index_file, "w") as fh:
		for key in library:
			fh.write("%s\tcustom\n" % key)
	data = {
		"path": path_to_script,
		"adapters": index_file,
		"input": settings["fastq_file"],
		"ok": settings["fastq_ok_file"],
		"bad": settings["fastq_bad_file"],
	}

	command = "%(path)s -i %(input)s -o %(ok)s -b %(bad)s --length 1 --polyG 100 --adapters %(adapters)s " % data
	print command
	os.system(command)

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Remove reads similar to sequences from fasta file.')
	parser.add_argument('-1','--reads1', help='Left file with reads', required=True)
	parser.add_argument('-f','--fasta', help='Fasta file with contaminations', required=True)
	parser.add_argument('-o','--ok', help='Fastq output for remaining reads', required=True)
	parser.add_argument('-b','--bad', help='Fastq output for filtered reads', required=True)
	parser.add_argument('-k','--k', help='K for kmers', required=False, default=23, type=int)
	
	args = vars(parser.parse_args())
	settings= {}
	settings["fastq_file"] = args["reads1"] 
	settings["fasta_file"] = args["fasta"]
	settings["fastq_ok_file"] = args["ok"]
	settings["fastq_bad_file"] = args["bad"]
	settings["k"] = int(args["k"])
	filter_reads_by_fasta(settings)