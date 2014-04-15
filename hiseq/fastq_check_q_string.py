#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from PyBioSnippets.hiseq.fastq_tools import check_quality_string_correctness
import argparse

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Check Q correctness.')
	parser.add_argument('-i','--input', help='Fastq file', required=True)
	args = vars(parser.parse_args())

	check_quality_string_correctness(args["input"])
