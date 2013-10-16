#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 29.01.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 

from trseeker.seqio.sam_file import sc_sam_reader

def main(settings):
    '''
    '''
    sam_file = settings["sam_file"]
    for sam_obj in sc_sam_reader(sam_file):
        print sam_obj.fragment_length

if __name__ == '__main__':
    main(settings)