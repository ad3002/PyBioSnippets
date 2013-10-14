#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
'''
Join fragmented fastq files from HiSeq.
'''

import os
import sys
import re
from collections import defaultdict
import argparse

def join_hiseq_files(folder, mask, remove=False):
	'''
	'''
	join_groups = defaultdict(list)
	for root, dirs, files in os.walk(folder, topdown=False):
		for name in files:
			if re.search(mask, name):
				apath = os.path.join(root, name)
				name_parts = name.split("_")
				similar_part = "_".join(name_parts[:4])
				join_groups[similar_part].append(apath)
	for name in join_groups:
		output_file = "%s.fastq" % name
		input_data = " ".join(join_groups[name])
		command = "cat %s > %s" % (input_data, output_file)
		print command
		os.system(command)
		if remove:
			command = "rm %s" input_data
			print command
			os.system(command)

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Join splitted fastq files.')
	parser.add_argument('-r','--remove', help='Remove files after joining', required=False)
	parser.add_argument('-i','--input', help='Input folder', required=True)
	parser.add_argument('-m','--mask', help='File mask', required=True)
	args = vars(parser.parse_args())
	join_hiseq_files(args["input"], args["mask"], remove=args["remove"])