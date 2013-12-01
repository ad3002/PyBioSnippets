#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from trseeker.seqio.fasta_file import sc_iter_fasta
import argparse

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Check presence of adapter kmers.')
	parser.add_argument('-i','--input', help='Fasta input', required=True)
	parser.add_argument('-o','--output', help='Fixed output', required=True)
	args = vars(parser.parse_args())

	
	fasta = args["input"]
	output = args["output"]
	
	with open(output, "w") as fh:
		for i, seq_obj in enumerate(sc_iter_fasta(fasta)):
			print i, "fix", seq_obj.seq_head
			seq_obj.seq_head = ">%s\n" % i
			fh.write(seq_obj.fasta)
