#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 29.01.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 

from trseeker.seqio.sam_file import sc_sam_reader
from collections import defaultdict

def compute_fragments_statistics(settings):
    '''
    '''
    sam_file = settings["sam_file"]
    lengths = defaultdict(int)
    for sam_obj in sc_sam_reader(sam_file):
         lengths[sam_obj.fragment_length] += 1

if __name__ == '__main__':
    compute_fragments_statistics(settings)