#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from trseeker.seqio.tab_file import sc_read_simple_tab_file

def count_unmapped(sam_file):
	''' Print number of unmapped reads in sam_file.
	'''
	mapped = 0
	unmapped = 0
	for data in sc_read_simple_tab_file(sam_file):
		read_id = data[0]
		match = data[2]
		if match == "*":
			unmapped += 1
		else:
			mapped += 1
		print unmapped, mapped, "\r",
	print 
	print "Unmapped %s from %s mapped" % (unmapped, mapped)
	return (mapped, unmapped)
	
def save_unmapped_to_fasta(sam_file, fasta_file):
	''' Save unmapped reads to file.
	'''
	print "Read data"
	with open(sam_file) as fh:
		datas = fh.readlines()
	with open(fasta_file, "w") as fh:
		for i, data in enumerate(datas):
			print i, "\r",
			data = data.strip().split("\t")
			head = data[0].strip()
			gid = data[2].strip()
			seq = data[9].strip()
			if gid == "*":
				fh.write(">%s\n%s\n" % (head, seq))
	print