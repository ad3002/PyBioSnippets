#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 29.01.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 

from trseeker.seqio.sam_file import sc_sam_reader
from collections import defaultdict
from trseeker.tools.draw_tools import draw_distribution_plot

def compute_fragments_statistics(settings):
    '''
    '''
    sam_file = settings["sam_file"]
    image_file = settings["image_file"]
    lengths = defaultdict(int)
    for sam_obj in sc_sam_reader(sam_file):
         lengths[sam_obj.fragment_length] += 1
    draw_distribution_plot(lengths, image_file)

if __name__ == '__main__':
    compute_fragments_statistics(settings)