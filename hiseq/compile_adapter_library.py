#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from trseeker.tools.ngrams_tools import compute_kmers_libraries_from_fasta
from trseeker.seqio.fasta_file import sc_iter_fasta
import cPickle

settings = {
	"illumina_adapters_file": "/home/akomissarov/libs/illumina.fa",
	"ks": [13, 23, 31], 
	"pickle_libraries_file": "/home/akomissarov/libs/illumina.pickle",
}

def create_conatmination_lib(settings):
	'''
	'''
	fasta_file = settings["illumina_adapters_file"]
	output_file = settings["pickle_libraries_file"]
	k_diaposon = settings["ks"]	
	libraies = compute_kmers_libraries_from_fasta(fasta_file, k_diaposon)
	with open(output_file, "w") as fh:
		cPickle.dump(libraies, fh)


