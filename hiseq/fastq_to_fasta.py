#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from PyBioSnippets.hiseq.fastq_tools import fastq_to_fasta
import argparse

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Convert fastq tp fasta.')
	parser.add_argument('-i','--input', help='Fastq file', required=True)
	parser.add_argument('-o','--output', help='Fasta output file', required=True)
	args = vars(parser.parse_args())

	fastq_to_fasta(args["input"], args["output"])
	