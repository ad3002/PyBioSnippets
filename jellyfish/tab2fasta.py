#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

def tab_file_to_fasta_file(tab_file, fasta_file, limit):
	''' Convert jellyfish tab data files in fasta file. 
	'''
	with open(tab_file) as fh:
		with open(fasta_file, "w") as fw:
			result = []
			for i, line in enumerate(fh):
				data = line.strip().split("\t")
				s = ">%s\n%s" % (i, data[0])
				result.append(s)
				if i == limit:
					break
			fw.write("\n".join(result))

if __name__ == '__main__':

	if len(sys.argv) != 4:
		print "Usage: name.py tab_file fasta_file limit"
		exit(0)
	else:
		tab_file = sys.argv[1]
		fasta_file = sys.argv[2]
		limit = sys.argv[3]
	tab_file_to_fasta_file(tab_file, fasta_file, limit)
