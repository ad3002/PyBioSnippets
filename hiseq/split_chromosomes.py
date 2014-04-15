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

	parser = argparse.ArgumentParser(description='Parse multi fasta.')
	parser.add_argument('-i','--input', help='Fasta input', required=True)
	parser.add_argument('-o','--output', help='Output prefix', required=True)
	args = vars(parser.parse_args())


	fasta = args["input"]
	output = args["output"]

	for i, seq_obj in enumerate(sc_iter_fasta(fasta, lower=False)):
		name = seq_obj.header.split()[0]
		print name
		with open("%s.%s.fa" % (output, name), "w") as fh:
			fh.write(seq_obj.fasta)