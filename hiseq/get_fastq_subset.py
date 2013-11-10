#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 23.02.2011
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 


from trseeker.seqio.sra_file import fastq_reader

fastq_file = "/stripe2/assembly_test/Caenorhabditis_elegans/raw_reads/DRR008443_500bp_1.fastq"
output_fastq_file = "/stripe2/assembly_test/Caenorhabditis_elegans/raw_reads/500K_1.fastq"

with open(output_fastq_file, "w") as fh:
	for i, read in enumerate(fastq_reader(fastq_file)):
		print i, "\r",
		if i == 500000:
			break
		fh.write(read.fastq)

fastq_file = "/stripe2/assembly_test/Caenorhabditis_elegans/raw_reads/DRR008443_500bp_2.fastq"
output_fastq_file = "/stripe2/assembly_test/Caenorhabditis_elegans/raw_reads/500K_2.fastq"

with open(output_fastq_file, "w") as fh:
	for i, read in enumerate(fastq_reader(fastq_file)):
		print i, "\r",
		if i == 500000:
			break
		fh.write(read.fastq)