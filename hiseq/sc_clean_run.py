#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
'''
'''

import os
import sys
import re
from collections import defaultdict
import argparse
import cPickle
from trseeker.tools.sequence_tools import get_revcomp
from trseeker.seqio.tab_file import sc_read_simple_tab_file


if __name__ == '__main__':
	
	settings = {
		"pickle_libraries_file": "/home/akomissarov/Dropbox/PyBioSnippets/hiseq/illumina.pickle",
	}

	parser = argparse.ArgumentParser(description='Clean single run.')
	parser.add_argument('-i','--input', help='Input fastq file', required=True)
	parser.add_argument('-o','--output', help='Output ok reads', required=True)
	parser.add_argument('-b','--bad', help='Output bad reads', required=True)
	
	args = vars(parser.parse_args())
	settings["fastq_file"] = args["input"] 
	settings["output_file"] = args["output"]
	settings["output_bad_file"] = args["bad"]
	check_adapters(settings)