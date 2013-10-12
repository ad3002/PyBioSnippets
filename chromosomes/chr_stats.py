#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from trseeker.seqio.fasta_file import sc_iter_fasta

def get_chromosome_lengths(rerence_multifasta):
    ''' Get chromosome lengths.
    @param rerence_multifasta: multifasta file with chromosomes
    @return: dictionary chr name -> chr length
    '''
    print "Read reference genome"
    chrs = {}
    for seq_obj in sc_iter_fasta(rerence_multifasta):
        chrs[seq_obj.seq_gi] = seq_obj.seq_length 
        chrs[seq_obj.seq_gi] = seq_obj.seq_length
    print chrs

def split_scaffolds_into_contigs(scaffolds_file, contigs_file):
    ''' Split and write contigs file from scaffolds_file.
    '''
    raise NotImplemented
