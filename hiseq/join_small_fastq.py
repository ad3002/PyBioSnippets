#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import os
import sys
from PyExp import sc_iter_filepath_folder

folder = "/stripe/akomissarov/baikal_seal/original_raw/male"

data = []
for file_name in sc_iter_filepath_folder(folder):
	data.append(file_name)
	# print file_name.split("_")
result = {}
data.sort()
for line in data:
	key = "_".join(line.split("_")[:-1])
	# print key
	result.setdefault(key, [])
	result[key].append(line)
for key, v in result.items():
	# print key, v

	command = "nohup cat %s > %s.fastq &" % (" ".join(v), key)
	print command
	os.system(command)