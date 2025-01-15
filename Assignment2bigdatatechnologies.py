# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 19:57:44 2022

@author: aidan
"""
import json
import io
import os
import re
import sys
import neo4j
directory = os.getcwd()
print(directory)

sys.stdout = open('output.json', 'w+', encoding="cp437", errors='ignore')
output = open('output.json', 'w+', encoding="cp437", errors='ignore')
output2 = open('output2.json', 'w+', encoding="cp437", errors='ignore')
output3 = open('output3.json', 'w+', encoding="cp437", errors='ignore')
output4 = open('output4.json', 'w+', encoding="cp437", errors='ignore')
output5 = open('output5.json', 'w+', encoding="cp437", errors='ignore')
output6 = open('output6.json', 'w+', encoding="cp437", errors='ignore')
output7 = open('output7.json', 'w+', encoding="cp437", errors='ignore')

#removes numbering of each tweet
for lines in open('10000Tweets1.json', 'r', encoding="cp437", errors='ignore'):
    if not re.search("/\*", lines):
        output.write(lines)  
output.close()

#removes object id from the document because it isnt JSON format
for lines2 in open('output.json', 'r', encoding="cp437", errors='ignore'):
    if not re.search("ObjectId", lines2):
        output2.write(lines2)
output2.close()

#removes 
for lines3 in open('output2.json', 'r', encoding="cp437", errors='ignore'):
    if not re.search(r'^\s*$', lines3):
        output3.write(lines3)
output3.close()

#inserts a comma in between end of object and start of object
with open('output3.json', 'r', encoding="cp437", errors='ignore') as infile:
    data = infile.read()
    new_data = data.replace('}\n{', '},\n{')
    output4.write(new_data)
output4.close()

#removes whitespace
with open('output4.json', 'r', encoding="cp437", errors='ignore') as infile1:
    data1 = infile1.read()
    new_data1 = data1.replace('}, {', '},\n{') 
    output5.write(new_data1)
output5.close()

#removes numberlong because it does not meet json format
for lines2 in open('output5.json', 'r', encoding="cp437", errors='ignore'):
    if not re.search("NumberLong", lines2):
        output6.write(lines2)
output6.close()

#write objects into a list
with open('output6.json', 'r', encoding="cp437", errors='ignore') as infile1:
    data2 = infile1.read()
    json_data = json.loads(f'[{data2}]')
    with open('output7.json', 'w', encoding="cp437", errors='ignore') as fp:
            json_object = json.dumps(json_data, indent=4)
            fp.write(json_object)
output7.close()
