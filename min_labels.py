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

# script for minimizing labels got from ILDasm disassembly
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


	
f = open(in_fname)
lines = f.readlines()
f.close()

regions = [[]]
i = -1
for line in lines:
	stripped = line.strip()
	if len(stripped) > 8 and stripped[7] == ':' and stripped[:3] == 'IL_':
		si = stripped[3:7]
		ii = int(si, 16)
		if ii <= i:
			i = -1
			regions += [[]]
		else:
			i = ii
	regions[-1] += [line]
	

def clean_region( region ):
	text = ''.join(region)
	output = ""
	for line in region:
		stripped = line.lstrip()
		d = ' ' * (len(line) - len(stripped))
		if len(stripped) > 8 and stripped[7] == ':' and stripped[:3] == 'IL_':
			label = stripped[:7]
			if text.find(label) == text.rfind(label):
				output += d + ' '*8 + stripped[8:]
			else:
				output += d + stripped
		else:
			output += d + stripped
	return output
			
		
output = ""
for region in regions:
	output += clean_region( region )

f = open(out_fname, 'w')
f.write(output)
f.close()
