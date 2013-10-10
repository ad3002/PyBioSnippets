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

def join_hiseq_files(folder, mask):
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

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Usage: name.py input_folder mask"
		exit(0)
	else:
		folder = sys.argv[1]
		mask = sys.argv[2]
	join_hiseq_files(folder, mask)