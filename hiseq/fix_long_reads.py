#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2017
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
'''

'''

from collections import defaultdict, deque
import sys, re, os
from trseeker.seqio.fasta_file import sc_iter_fasta
import jellyfish
from trseeker.tools.jellyfish_tools import Kmer2tfAPI, Kmer2tfAPI2
import math
from PyBioSnippets.hiseq.fastq_tools import iter_pe_data
import argparse
from trseeker.tools.sequence_tools import get_revcomp
from trseeker.tools.edit_distance import hamming_distance
from collections import defaultdict
from trseeker.tools.jellyfish_tools import Kmer2tfAPI
from trseeker.seqio.sam_file import sc_sam_reader, sc_sam_get_headers
from trseeker.tools.ngrams_tools import print_next_cutoff
from trseeker.tools.ngrams_tools import print_prev_cutoff
from AriadnaPy.tools.unitigs import extend_to_right


def correct_read(read, kmer2tf, settings):

    ERROR_CUTOFF = settings["error_cutoff"]
    k = settings["k"]
    cov_map = []
    in_zero = None
    i = 0
    read = bytearray(read)
    cov_map = [0]*(len(read)-k+1)
    was_zero = False
    was_solid = False
    cigar = ""
    while i < len(read)-k+1:
        kmer = str(read[i:i+k])
        tf = kmer2tf[kmer]
        cov_map[i] = tf
        # print i, kmer, tf, print_next_cutoff(kmer, kmer2tf, cutoff=0)[0]
        # raw_input("?")
        if tf < ERROR_CUTOFF:   
            if not in_zero and was_solid:
                _kmer = str(read[i-1:i-1+k])
                Rr, nr, nucleotides, _ = print_next_cutoff(_kmer, kmer2tf, cutoff=settings["extension_error"])
                # print i, Rr, nr
                if nr == 1:
                    read[i+k-1] = nucleotides[0]
                    continue
                # elif nr > 1:
                #     fragment = read[i-3:i+k-1+k]
                #     def_error = 0
                #     covs = []
                #     for j in xrange(0,len(fragment)-k+1):
                #         tf = kmer2tf[str(fragment[j:j+k])]
                #         covs.append(tf)
                #         if tf < ERROR_CUTOFF:
                #             def_error += 1

                #     print str(fragment)
                #     print "FOR DEF", chr(read[i+k-1]), def_error
                #     print covs
                #     for nucl in nucleotides:
                #         fragment[k-1+3] = nucl
                #         print str(fragment), nucl, Rr[nucl]
                #         error = 0
                #         covs = []
                #         for j in xrange(0,len(fragment)-k+1):
                #             tf = kmer2tf[str(fragment[j:j+k])]
                #             if tf < ERROR_CUTOFF:
                #                 error += 1
                #                 R = print_next_cutoff(str(fragment[j-1:j+k-1]), kmer2tf, cutoff=settings["extension_error"])[0]
                #                 if R:
                #                     print R
                #             covs.append(tf)
                #         print nucl, error
                #         print covs
                #     raw_input("?")
                else:
                    # return read, "ERROR", []
                    print i, "FOR", Rr, nr
                    # raw_input("?")
                    # pass
            in_zero = True
            was_zero = True
            was_solid = False
        else:
            was_solid = True
            in_zero = False

        i += 1
    if was_zero:
        was_zero = False
        was_solid = False
        i = len(read)-k
        while i >= 0 :
            kmer = str(read[i:i+k])
            tf = kmer2tf[kmer]
            cov_map[i] = tf
            # print i, kmer, tf, print_next_cutoff(kmer, kmer2tf, cutoff=0)[0]
            # raw_input("?")
            if tf < ERROR_CUTOFF:
                if not in_zero and was_solid:
                    _kmer = str(read[i+1:i+1+k])
                    Rr, nr, nucleotides, _ = print_prev_cutoff(_kmer, kmer2tf, cutoff=settings["extension_error"])
                    # print i, Rr, nr
                    if nr == 1:
                        read[i] = nucleotides[0]
                        continue
                    # elif nr > 1:
                    #     start = max(0, i-k+1)
                    #     fragment = read[start:start+k-1+k]
                    #     def_error = 0
                    #     for j in xrange(0,len(fragment)-k+1):
                    #         tf = kmer2tf[str(fragment[j:j+k])]
                    #         if tf < ERROR_CUTOFF:
                    #             def_error += 1
                    #             # print print_next_cutoff(str(fragment[j-1:j+k-1]), kmer2tf, cutoff=settings["extension_error"])[0]
                    #     print "REV DEF", chr(read[i]), def_error
                    #     for nucl in nucleotides:
                    #         if i-k+1 >= 0:
                    #             fragment[k-1] = nucl
                    #         else:
                    #             fragment[k-1-(i-k+1)] = nucl
                    #         error = 0
                    #         for j in xrange(0,len(fragment)-k+1):
                    #             tf = kmer2tf[str(fragment[j:j+k])]
                    #             if tf < ERROR_CUTOFF:
                    #                 error += 1
                    #         print nucl, error
                    #     raw_input("?")
                    else:
                        # return read, "ERROR", []
                        # print i, "REV", Rr, nr
                        # raw_input("?")
                        pass
                in_zero = True
                was_zero = True
                was_solid = False
            else:
                was_solid = True
                in_zero = False
                
            i -= 1

    status = "OK"
    if was_zero:     
        print cov_map
        print str(read)
        status = "ERROR"
        pass
        raw_input("error?")
    else:
        # print cov_map
        # raw_input("ok?")
        pass
    return read, status, cov_map


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='PacBio assembly correction.')
    parser.add_argument('-1', help='Fastq file1', required=True)
    parser.add_argument('-2', help='Fastq file2', required=True)
    parser.add_argument('-s', help='Start', required=True)
    parser.add_argument('-e', help='End', required=True)
    parser.add_argument('-k', help='k', required=False, default=23)
    parser.add_argument('-c', help='errors', required=False, default=0)
    parser.add_argument('-j', help='Jf2 file', required=False, default=None)
    args = vars(parser.parse_args())
    
    k = int(args["k"])
    
    error_cutoff = int(args["c"])


    settings = {
        "hd_cutoff": error_cutoff,
        "error_cutoff": error_cutoff,
        "extension_error": error_cutoff,
        "k": k,
    }

    start_sid = int(args["s"])
    end_sid = int(args["e"])
    

    if args["j"]:
        jf_path = args["j"]
        jf_api = jellyfish.QueryMerFile(jf_path)
        kmer2tf = Kmer2tfAPI(jf_api)

    fastq1_file = args["1"]
    fastq2_file = args["2"]
    res_file_template = "result.fa"

    fastq1_file_ok = fastq1_file.replace("_1.fastq", ".ok_1.fastq")
    assert fastq1_file_ok != fastq1_file
    fastq2_file_ok = fastq2_file.replace("_2.fastq", ".ok_2.fastq")
    assert fastq2_file_ok != fastq2_file

    fastq1_file_err = fastq1_file.replace("_1.fastq", ".err_1.fastq")
    assert fastq1_file_err != fastq1_file
    fastq2_file_err = fastq2_file.replace("_2.fastq", ".err_2.fastq")
    assert fastq2_file_err != fastq2_file


    with open(fastq1_file_ok, "w") as fh:
        pass
    with open(fastq2_file_ok, "w") as fh:
        pass
    with open(fastq1_file_err, "w") as fh:
        pass
    with open(fastq2_file_err, "w") as fh:
        pass

    fh1 = open(fastq1_file_ok, "w")
    fh2 = open(fastq2_file_ok, "w")
    fe1 = open(fastq1_file_err, "w")
    fe2 = open(fastq2_file_err, "w")

    results = {
        "ok": 5,
        "errors": 5,
        "short": 5,
    }

    ok_results = []
    error_results = []

    for i, (read1, read2) in enumerate(iter_pe_data(fastq1_file, fastq2_file)):
        if i < start_sid:
            print "Skipped:", seq_obj.seq_head
            continue
        if i >= end_sid:
            print "Done"
            break

        read = read1.seq
        if len(read) > k:
            corrected_read1, status1, cov_map1 = correct_read(read, kmer2tf, settings)
        else:
            results["short"] += 1
            continue
            
        read = read2.seq
        if len(read) > k:
            corrected_read2, status2, cov_map2 = correct_read(read, kmer2tf, settings)
        else:
            results["short"] += 1
            continue
         

        read1.seq = corrected_read1
        read2.seq = corrected_read2

        if status1 == status2 == "OK":
            results["ok"] += 1

            read1.strain = "+"
            read2.strain = "+"

            fh1.write(read1.fastq)
            fh2.write(read2.fastq)

        else:
            results["errors"] += 1

            read1.strain = "+"
            read2.strain = "+"

            fe1.write(read1.fastq)
            fe2.write(read2.fastq)

   
        
        print i, results, round(100.*(results["errors"]+1)/(i+1),2)

   

    fh1.close()
    fh2.close()
    fe1.close()
    fe2.close()
