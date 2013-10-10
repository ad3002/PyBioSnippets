#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from trseeker.tools.jellyfish import query_and_write_coverage_histogram

def main(jellyfish_db, output_file, query_sequence, k):
	query_and_write_coverage_histogram(jellyfish_db, query_sequence, output_file, k=k)

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print "Usage: name.py jellyfish_db output_file k query_sequence)"
		exit(0)
	else:
		jellyfish_db = sys.argv[1]
		output_file = sys.argv[2]
		k = sys.argv[3]
		query_sequence = sys.argv[4]
		
	main(jellyfish_db, output_file, query_sequence, k)