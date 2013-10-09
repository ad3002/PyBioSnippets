#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
from collections import defaultdict

def compute_histogram(data_tab_file):
	'''
	'''
	D = defaultdict(int)
	with open(data_tab_file) as fh:
		for line in fh:
			data = line.strip().split("\t")
			D[int(data[1])] += 1


