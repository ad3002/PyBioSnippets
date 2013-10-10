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
from collections import defaultdict

def join_hiseq_files(folder):
	'''
	'''
	join_groups = defaultdict(list)
	for root, dirs, files in os.walk(folder, topdown=False):
		for name in files:
			if re.search(self.mask, name):
				apath = os.path.join(root, name)
				name_parts = name.split("_")
				similar_part = "_".join(name[:4])
				join_groups[similar_part].append(apath)
	print join_groups

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: name.py input_folder"
		exit(0)
	else:
		folder = sys.argv[1]
	join_hiseq_files(folder)