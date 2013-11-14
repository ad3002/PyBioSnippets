#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 29.01.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 

from trseeker.seqio.sam_file import sc_sam_reader
from collections import defaultdict
from trseeker.tools.draw_tools import draw_distribution_plot
import argparse

def main(settings, limit=None):
    '''
    '''
    sam_file = settings["sam_file"]
    results = defaultdict(int)
    for i, sam_obj in enumerate(sc_sam_reader(sam_file)):
        results[sam_obj.FLAG] += 1
        print results, "\r",    
    print 
    print "results", results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute fragments from SAM file.')
    parser.add_argument('-i','--input', help='Input SAM file', required=True)
    args = vars(parser.parse_args())
    settings = {
        "sam_file": args["input"],
    }
    main(settings)