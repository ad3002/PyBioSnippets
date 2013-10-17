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

def compute_fragments_statistics(settings, limit=None):
    '''
    '''
    sam_file = settings["sam_file"]
    image_file = settings["image_file"]
    lengths = defaultdict(int)
    zeros = 0
    if not limit:
        print "Process full SAM file..."
    else:
        print "Process %s lines from SAM file..." % limit
    for i, sam_obj in enumerate(sc_sam_reader(sam_file)):
        print i, "\r",
        if limit and i > limit:
            break
        if sam_obj.fragment_length > 0:
            lengths[sam_obj.fragment_length] += 1
        else:
            zeros += 1
    keys = lengths.keys()
    keys.sort()
    for k in keys:
        print k, lengths[k], round(100.*lengths[k]/i, 3)
    print "Write image to %s" % image_file
    draw_distribution_plot(lengths, image_file)
    print "Fragments of zero length: %s" % zeros

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute fragments from SAM file.')
    parser.add_argument('-o','--ouput', help='Output image', required=True)
    parser.add_argument('-i','--input', help='Input SAM file', required=True)
    parser.add_argument('-l','--limit', help='Only first l lines', required=False, default=0, type=int)
    args = vars(parser.parse_args())
    settings = {
        "sam_file": args["input"],
        "image_file": args["ouput"],
    }
    compute_fragments_statistics(settings, limit=args["limit"])