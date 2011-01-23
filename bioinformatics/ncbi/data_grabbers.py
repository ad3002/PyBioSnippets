#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 17.01.2011
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com 
#@license: Creative Commons Attribution License

'''
    FAQ
    1. How to get all sequenced prokaryotic genomes?
    >>> n, genome_objs = get_ncbi_genome_list_page("PRO")
    2. How to get all sequenced eukaryotic genomes?
    >>> n, genome_objs = get_ncbi_genome_list_page("EU")
    3. How to get number of sequenced virus genomes?
    >>> n, genome_objs = get_ncbi_genome_list_page("VIRI")
    4. How to get number of sequenced metagenomes?
    >>> n, genome_objs = get_ncbi_genome_list_page("META")
    5. How to get the number genomes per year?
    >>> print_genome_per_year(genome_objs)
    6. How to get mammals genomes only?
    >>> n, genome_objs = get_ncbi_genome_list_page("EU")
    >>> genome_objs = [x for x in genome_objs if x.subgroup == "Mammals"]
    7. How to get human genomes only?
    >>> n, genome_objs = get_ncbi_genome_list_page("EU")
    >>> genome_objs = [x for x in genome_objs if "Homo sapiens" in x.taxon]

'''

import urllib2
import re

url_ncbi_wgs_list = "http://www.ncbi.nlm.nih.gov/projects/WGS/WGSprojectlist.cgi"
url_ncbi_eu_genome_list = "http://www.ncbi.nlm.nih.gov/genomes/leuks.cgi"
url_ncbi_pro_genome_list = "http://www.ncbi.nlm.nih.gov/genomes/lproks.cgi"
url_ncbi_meta_genome_list = "http://www.ncbi.nlm.nih.gov/genomes/lenvs.cgi"
url_ncbi_viri_genome_list = "http://www.ncbi.nlm.nih.gov/genomes/GenomesGroup.cgi?taxid=10239&opt=Virus"

re_font_item = u"<font[^>]*>(.*?)</font>"
re_td_item = u"<td[^>]*>(.*?)</td>"
re_a_item = u"<a.*?href=\"(.*?)\"[^>]*>(.*?)</a>"

class VirusProjectData(object):
    '''
    Container with virus genome information
    '''
    taxon = None
    acc = None
    source = None
    segm = None
    genome_size = None
    proteins = None
    nbrs = None
    released = None
    modified = None

class WGSProjectData(object):
    '''
    Container with WGS assembly information
    '''
    prefix = None
    gpid = None
    taxon = None
    contigs = 0 
    cons = 0
    annotation = None
    complete = None

class EuGenomeProjectData(object):
    '''
    Container with eukaryotic genome information
    '''
    gpid = None
    taxon = None
    group = None
    subgroup = None
    taxid = None
    genome_size = None
    chr_n = None
    status = None
    method = None
    depth = None
    released = None
    center = None
    
class ProGenomeProjectData(object):
    '''
    Container with prokaryotic genome information
    '''
    pid = None
    gpid = None
    taxon = None
    king = None
    group = None
    genome_size = None
    gc = None
    chr_n = None
    plasmids = None
    gb = None
    refseq = None
    released = None
    modified = None
    center = None
        
class MetaGenomeProjectData(object):
    '''
    Container with metagenomics information
    '''
    overview_id = None
    gpid = None
    title = None
    type = 0 
    source = 0
    acc = None
    released = None
    center = None
    blast = None
    trace = None

def parse_link(element, reg_exp=None):
    
    if not reg_exp:
        reg_exp = re_a_item
    match_obj = re.search(reg_exp, element, re.S|re.I)
    if match_obj:
        return match_obj.group(2)
    return element


def parser_ncbi_viri_genome_list(page):
    '''
    Function parses a page with virus genomes 
    and return #genomes, list of genome's info containers.
    '''
    re_tr_item = u"<tr bgcolor=\"#F.*?\">(.*?)</tr>"
    items = re.findall(re_tr_item, page, re.S|re.I)
    
    print "Number of projects :", len(items)
    
    result = []
    
    for i, item in enumerate(items):
        
        obj = VirusProjectData()
        
        data = re.findall(re_td_item, item, re.S|re.I)
        
        if len(data)<8:
            continue
        print i,
        
        for j, element in enumerate(data):
            
            element = element.replace(u"&nbsp;","").strip()
            
            if j == 0:
                match_obj = re.findall(re_a_item, element, re.S)
                if match_obj:
                    if '<img border="0" src="/sutils/static/GP_IMAGE/plus.png"' in element:
                        obj.taxon = match_obj[1][1]
                    else:
                        obj.taxon = match_obj[0][1]
                print obj.taxon,
            elif j == 1:
                obj.acc = parse_link(element)
                print obj.acc,
            elif j == 2:
                obj.source = element
                print obj.source,
            elif j == 3:
                obj.segm = element
                print obj.segm,
            elif j == 4:
                element = element.replace(u"nt","").strip()
                obj.genome_size = element
                print obj.genome_size,
            elif j == 5:
                obj.proteins = parse_link(element)
                print obj.proteins,
            elif j == 6:
                obj.nbrs = parse_link(element)
                print obj.nbrs,
            elif j == 7:
                obj.released = element
                print obj.released,
            elif j == 8:
                obj.modified = element
                print obj.modified
        if obj.released:   
            result.append(obj)
    return len(result), result

def parser_ncbi_wgs_list(page):
    '''
    Function parses a page with WGS assemblies 
    and return #wgs, list of WGS's info containers.
    '''
    re_genome_item = u"-->\s*<TR>.*?</TR>"
    re_a_item_local = u"<A.*?HREF=\"?(.*?)\"?[^>]*>(.*?)</A>"
    
    items = re.findall(re_genome_item, page, re.S|re.I)
    print "Number of projects :", len(items)
    
    result = []
    
    for i, item in enumerate(items):
        
        data = re.findall(re_td_item, item, re.S|re.I)
        obj = WGSProjectData()
        print i,
        for j, element in enumerate(data):
            element = element.replace(u"&nbsp;","").strip()
            element = element.replace(u"<B>","").strip()
            element = element.replace(u"</B>","").strip()
            if j == 1:
                obj.prefix = parse_link(element, reg_exp=re_a_item_local)
                print obj.prefix,
            elif j == 2:
                obj.gpid = parse_link(element, reg_exp=re_a_item_local)
                print obj.gpid,
            elif j == 4:
                obj.taxon = parse_link(element, reg_exp=re_a_item_local)
                print obj.taxon,
            elif j == 5:
                element = element.replace(",","")
                element = element.replace("-","")
                if element:
                    obj.contigs = int(element.strip())
                print obj.contigs,
            elif j == 6:
                element = element.replace(",","")
                element = element.replace("-","")
                if element:
                    obj.cons = int(element.strip())
                print obj.cons,
            elif j == 7:
                element = element.replace(",","")
                element = element.replace("-","")
                if element:
                    obj.annotation = int(element.strip())
                print obj.annotation,
            elif j == 8:
                obj.complete = parse_link(element, reg_exp=re_a_item_local)
                print obj.complete
        if obj.prefix:
            result.append(obj)
    return len(result), result

def parser_ncbi_meta_genome_list(page):
    '''
    Function parses a page with virus genomes 
    and return #genomes, list of genome's info containers.
    '''
    re_tr_item = u"<tr class=\"trcolor.\">(.*?)</tr>"
    items = re.findall(re_tr_item, page, re.S|re.I)
    
    print "Number of projects :", len(items)
    
    result = []
    for i, item in enumerate(items):
        obj = MetaGenomeProjectData()
        data = re.findall(re_td_item, item, re.S|re.I)
        print i,
        for j, element in enumerate(data):
            element = element.replace(u"&nbsp;","").strip()
            if j == 0:
                obj.overview_id = parse_link(element)
                print obj.overview_id,
            elif j == 1:
                obj.gpid = parse_link(element)
                print obj.gpid,
            elif j == 2:
                obj.title = parse_link(element)
                print obj.title,
            elif j == 3:
                obj.type = element
                print obj.type, 
            elif j == 4:
                obj.source = parse_link(element)
                print obj.source,
            elif j == 5:
                obj.acc = parse_link(element)
                print obj.acc,
            elif j == 6:
                element = element.replace(u"<b>","").strip()
                element = element.replace(u"</b>","").strip()
                obj.released = element
                print obj.released,   
            elif j == 7:
                obj.center = parse_link(element)
                print obj.center, 
            elif j == 8:
                obj.blast = parse_link(element)
                if u"</font>" in obj.blast:
                    match_obj = re.search(re_font_item, obj.blast, re.S|re.I)
                    obj.blast = match_obj.group(1)
                print obj.blast, 
            elif j == 9:
                obj.trace = parse_link(element)
                if u"</font>" in obj.trace:
                    match_obj = re.search(re_font_item, obj.trace, re.S|re.I)
                    obj.trace = match_obj.group(1)
                print obj.trace
        if obj.gpid:
            result.append(obj)
    return len(result), result
    
def parser_ncbi_pro_genome_list(page):
    '''
    Function parses a page with virus genomes 
    and return #genomes, list of genome's info containers.
    '''
    re_tr_item = u"<tr bgcolor=\"#E.*?\">(.*?)</tr>"
    items = re.findall(re_tr_item, page, re.S|re.I)
    print "Number of projects :", len(items)
    
    result = []
    
    for i, item in enumerate(items):
        obj = ProGenomeProjectData()
        data = re.findall(re_td_item, item, re.S|re.I)
        print i,
        for j, element in enumerate(data):
            element = element.replace(u"&nbsp;","").strip()
            if j == 0:
                obj.pid = parse_link(element)
                print obj.pid,
            elif j == 1:
                obj.gpid = parse_link(element)
                print obj.gpid,
            elif j == 2:
                obj.taxon = parse_link(element)
                print obj.taxon,
            elif j == 3:
                if u"</font>" in element:
                    match_obj = re.search(re_font_item, element, re.S|re.I)
                    element = match_obj.group(1)
                obj.king = element
                print obj.king,
            elif j == 4:
                obj.group = element
                print obj.group,
            elif j == 5:
                element = element.replace(u'<sup style="font-size: smaller; font-weight: bold; color: red">*</sup>',"").strip()
                element = element.replace(u"</b>","").strip()
                element = element.replace(u"<b>","").strip()
                obj.genome_size = element
                print obj.genome_size,
            elif j == 6:
                element = element.replace(u"<b>","").strip()
                element = element.replace(u"</b>","").strip()
                obj.gc = element
                print obj.gc,  
            elif j == 7:
                element = element.replace(u"<b>","").strip()
                element = element.replace(u"</b>","").strip()
                obj.chr_n = element
                print obj.chr_n, 
            elif j == 8:
                element = element.replace(u"<b>","").strip()
                element = element.replace(u"</b>","").strip()
                obj.plasmids = element
                print obj.plasmids,
            elif j == 9:
                obj.gb = parse_link(element)
                print obj.gb,
            elif j == 10:
                obj.refseq = parse_link(element)
                print obj.refseq,
            elif j == 11:
                element = element.replace(u"<b>","").strip()
                element = element.replace(u"</b>","").strip()
                obj.released = element
                print obj.released,
            elif j == 12:
                element = element.replace(u"<b>","").strip()
                element = element.replace(u"</b>","").strip()
                obj.modified = element
                print obj.modified,
            elif j == 13:
                obj.center = parse_link(element)
                print obj.center
        if obj.gpid:   
            result.append(obj)
    return len(result), result
    
def parser_ncbi_eu_genome_list(page):
    '''
    Function parses a page with virus genomes 
    and return #genomes, list of genome's info containers.
    '''
    re_tr_item = u"<tr class=\"trcolor.\">(.*?)</tr>"
    items = re.findall(re_tr_item, page, re.S|re.I)
    print "Number of projects :", len(items)
    
    result = []
    
    for i, item in enumerate(items):
        obj = EuGenomeProjectData()
        data = re.findall(re_td_item, item, re.S|re.I)
        print i,
        for j, element in enumerate(data):
            element = element.replace(u"&nbsp;","").strip()
            if j == 0:
                obj.gpid = parse_link(element)
                print obj.gpid,            
            elif j == 1:
                obj.taxon = parse_link(element)
                print obj.taxon,
            elif j == 2:
                obj.group = element
                print obj.group,
            elif j == 3:
                obj.subgroup = element
                print obj.subgroup, 
            elif j == 4:
                obj.taxid = parse_link(element)
                print obj.taxid,
            elif j == 5:
                obj.genome_size = element
                print obj.genome_size,
            elif j == 6:
                obj.chr_n = element
                print obj.chr_n,  
            elif j == 7:
                obj.status = element
                print obj.status,
            elif j == 8:
                obj.method = element
                print obj.method,
            elif j == 9:
                obj.depth = element
                print obj.depth,
            elif j == 10:
                obj.released = element
                print obj.released,
            elif j == 11:
                obj.center = parse_link(element)
                print obj.center
        if obj.gpid:
            result.append(obj)
    return len(result), result
    
parsers_functions = {"WGS":parser_ncbi_wgs_list,
           "PRO":parser_ncbi_pro_genome_list,
           "EU":parser_ncbi_eu_genome_list,
           "VIRI":parser_ncbi_viri_genome_list,
           "META":parser_ncbi_meta_genome_list,
           }

ncbi_pages = {"WGS":url_ncbi_wgs_list,
           "PRO":url_ncbi_pro_genome_list,
           "EU":url_ncbi_eu_genome_list,
           "VIRI":url_ncbi_viri_genome_list,
           "META":url_ncbi_meta_genome_list,
           }    
    
def get_ncbi_genome_list_page(parser):
    result = urllib2.urlopen(ncbi_pages[parser])
    page = result.read().decode('iso-8859-1')
    n, data = parsers_functions[parser](page)
    return n, data

def print_genome_per_year(data):
    per_year = {}
    for x in data:
        y = x.released.split("/")[-1]
        per_year.setdefault(y, 0)
        per_year[y] += 1
    for x, i in per_year.items():
        print x, i
    
if __name__ == '__main__':
    pass
    
        
            
    