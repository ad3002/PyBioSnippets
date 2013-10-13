#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from PyBioSnippets.hiseq.fastq_tools import separate_reads_witn_n_and_sharps

separate_reads_witn_n_and_sharps(fastq_file, output_file, reads_with_n_file, reads_with_sharp_file)

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Usage: name.py input_folder mask"
		exit(0)
	else:
		folder = sys.argv[1]
		mask = sys.argv[2]
	join_hiseq_files(folder, mask)