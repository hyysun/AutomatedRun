__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call, Popen, PIPE, STDOUT

# Step1: Put the file names in a text file as the inputfile

# Assume that all files have been uploaded in the hadoop cluster 
# dir should be a hdfs directory
dir = sys.argv[1]

cmd = 'hadoop fs -ls '+ dir
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
content = p.stdout.read()
files = content.split('\n')
tmpfile = open(os.path.join('./', 'input.txt'),'w')

for file in files:
    file = file.split(' ')
    fname = file[len(file)-1]
    fname = 'hdfs://icme-hadoop1.localdomain' + fname
    if fname.endswith('.e'):
         tmpfile.write("%s\n" % fname)
  
tmpfile.close()
       
inputfile = os.path.join(dir,'input.txt')
if call(['hadoop', 'fs', '-test', '-e', inputfile]) == 0:
    check_call(['hadoop', 'fs', '-rm', inputfile])
check_call(['hadoop', 'fs', '-copyFromLocal', os.path.join('./','input.txt'), inputfile])

check_call(['rm', os.path.join('./', 'input.txt')])
