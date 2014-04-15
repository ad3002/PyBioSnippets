#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from trseeker.seqio.sra_file import fastq_reader
import argparse

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Remove reads with N.')
	parser.add_argument('-i','--input', help='Fastq file', required=True)
	parser.add_argument('-o','--output', help='Fastq file', required=True)
	args = vars(parser.parse_args())
	print "Process data"
	data = []
	ok = 0
	l = int(args["length"])
	with open(args["output"], "w") as fh:
		for i, read in enumerate(fastq_reader(args["input"])):
			if i % 10000 == 0:
				print ok, i, ok/(i+1.), "\r",
			if 'N' in read.seq:
				continue
			fh.write(read.fastq)
			ok += 1
	print
	print "Final: saved %s (%s) from %s" % (ok, ok/(i+1.), i)
	