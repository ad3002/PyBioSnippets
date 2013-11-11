#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
'''
Convert raw pacbio bax.h5 files to fastq and fasta files.

You need:
1) https://github.com/PacificBiosciences/pbcore
2) https://github.com/ad3002/PyExp

'''
import sys
from pbcore.io import CmpH5Reader
from pbcore.io import BasH5Reader
from PyExp import sc_iter_filepath_folder

def pacbio_raw_to_fastq_and_fasta(file_name, phred=33):
    ''' Convert pacbio bax.h5 files to fasta and fastq files.

    @params file_name: prefix for processed file
    @param phred: phred offset (default 33)
    '''
    fastq_file = file_name+".fastq"
    fasta_file = file_name+".fasta"
    i = 0
    with open(fastq_file, "w") as fastq_fh:
        with open(fasta_file, "w") as fasta_fh:
            print "Read data..."
            with BasH5Reader(file_name) as r:
                for zmv in r:
                    for subread in zmv.subreads:
                        i += 1
                        print file_name, i, "\r",
                        header = subread.readName
                        seq = subread.basecalls().lower()
                        quals ="".join([chr(x+phred) for x in subread.InsertionQV()])
                        fastq = "@%s\n%s\n%s\n%s\n" % (header, seq, "+", quals)
                        fastq_fh.write(fastq)
                        fasta = ">%s\n%s\n" % (header, seq)
                        fasta_fh.write(fasta)
            print file_name, i, "DONE"

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: program_name file_name.bax.h5"
		exit(0)
    file_name = sys.argv[1]
    pacbio_raw_to_fastq_and_fasta(file_name, phred=33)