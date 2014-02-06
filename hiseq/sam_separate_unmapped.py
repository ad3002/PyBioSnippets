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
    output_file = settings["output_file"]
    
    unmapped = 0
    with open(output_file, "w") as fh:
        for i, sam_obj in enumerate(sc_sam_reader(sam_file)):
            if sam_obj.RNAME == "*":
                fh.write(sam_obj.as_sam())
                unmapped += 1    
            print i, unmapped, "\r",
    print 
    print "Unmapped fraction:", float(unmapped)/(i+1)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute fragments from SAM file.')
    parser.add_argument('-i','--input', help='Input SAM file', required=True)
    parser.add_argument('-o','--output', help='Output SAM file', required=True)
    args = vars(parser.parse_args())
    settings = {
        "sam_file": args["input"],
        "output_file": args["output"],
    }
    main(settings)