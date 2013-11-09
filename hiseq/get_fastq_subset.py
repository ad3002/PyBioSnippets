#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 23.02.2011
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 


from trseeker.seqio.sra_file import fastq_reader

fastq_file = "/stripe/akomissarov/aurelia_aurita/raw_reads/raw_reads.fastq"
output_fastq_file = "/stripe/akomissarov/aurelia_aurita/raw_reads/1M.fastq"

with open(output_fastq_file, "w") as fh:
	for i, read in enumerate(fastq_reader(fastq_file)):
		print i, "\r",
		if i == 1000000:
			break
		fh.write(read.fastq)