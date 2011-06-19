#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 07.02.2011
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 

import re
import urllib2
from genome_list_scrapper import get_ncbi_genome_list_page
import pickle

taxonomy_block = "<!--  the contents   -->(.*?)</td>" 
taxons = " TITLE=\"([^\"]*?)\">([^<]*?)</a>"

taxons_alt = "TITLE=\"([^\"]*?)\" ALT=\"[^\"]*?\">([^<]*?)</A>"

def taxonomy_parser(page):
    blocks = re.findall(taxons, page, re.S|re.I)
    if not blocks:
        blocks = re.findall(taxons_alt, page, re.S|re.I)
    return blocks

def get_taxons(taxid):
    url = "http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=%s" % taxid
    result = urllib2.urlopen(url)
    page = result.read().decode('iso-8859-1')
    data = taxonomy_parser(page)
    return data

n, objs = get_ncbi_genome_list_page("EU")
for obj in objs:
    obj.taxons_path = get_taxons(obj.taxid)
    print obj.taxon, obj.taxid, obj.taxons_path
    
pickle.dump(objs, open("eu_genomes.pickle", "w"))