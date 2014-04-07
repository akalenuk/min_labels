#!/usr/bin/python
#
# Copyright 2014 Alexandr Kalenuk.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# mailto: akalenuk@gmail.com

import sys

if len(sys.argv) < 2:
	print "Provide an input file name at least"
	exit(1)
elif len(sys.argv) == 2:
	in_fname = sys.argv[1]
	out_fname = in_fname + '.min_labels'
elif len(sys.argv) == 3:	
	in_fname = sys.argv[1]
	out_fname = sys.argv[2]
else:
	print "Too many paramenters"
	exit(1)

def clean( text ):
	lines = []
	labels = set()
	double_labels = set()
	
	for line in text.split('\n'):
		lines += line.rstrip()
		line = line.replace('\t', ' ').lstrip()

		label_or_not = line.split(' ')[0]
		if label_or_not != '' and label_or_not[-1] == ':':
			labels.add(label_or_not)
	
	for label in labels:
		text2 = text.replace(label[:-1], '')
		if len(text) - len(text2) > len(label)-1:
			double_labels.add(label)

	unique_labels = labels - double_labels

	for ulabel in unique_labels:
		text = text.replace(ulabel, '        ')
		
	return text

	
f = open(in_fname)
text = ''.join(f.readlines())
f.close()

output = ""
in_brackets = ""
depth = 0

for c in text:
	if c == '{':
		depth += 1
	elif c == '}':
		depth -= 1
		if depth == 0:
			output += clean( in_brackets )
			in_brackets = ""

	if depth == 0:
		output += c
	else:
		in_brackets += c
	
f = open(out_fname, 'w')
f.write(output)
f.close()
