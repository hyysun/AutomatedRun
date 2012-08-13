"""
Automate run

History
-------
:2012-08-07: initial coding

Example:

python automate.py hdfs://icme-hadoop1.localdomain/user/yangyang/simform/ \
--variables TEMP --varname Global_Variance \
--template thermal_maze0001.e --output tempglobalvar.e 

"""

__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call, Popen, PIPE, STDOUT
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--variables', dest='variables',
    help='--variables VARS, Only output the variables in the comma delimited list')
            
parser.add_option('-t', '--timesteps', dest='timesteps', default = 10,
    help='-t NUM or --timesteps NUM, Groups the output into batches of NUM timesteps')
            
parser.add_option('-d', '--dir', dest='outdir', default = '',
    help='-d DIR or --outdir DIR, Write the output to the directory DIR')
            
parser.add_option('--template', dest='template',
    help='--template FILE, the template exodus file')
            
parser.add_option('-o', '--output', dest='output',
    help='-o FILE or --output FILE, the new exodus file')
            
parser.add_option('--tmpdir', dest='tmpdir', default = './',
    help='--tmpdir PATH, the temporary directory')
            
parser.add_option('--varname', dest='varname',
    help='--varname NAME, the name of the variable in the exodus file')
            
(options, args) = parser.parse_args()

# Assume that all files have been uploaded in the hadoop cluster 
# dir should be a hdfs directory
dir = sys.argv[1]
if options.outdir == '':
    options.outdir = os.path.join(dir,'seqdata5')
    
# Step1: Put the file names in a text file as the inputfile

print 'Preprocessing...'

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

print 'Done!'

# Step2: Convert exodus files to sequence files

print 'Converting exodus files to sequece files...'

check_call(['time', 'python', 'mr_exodus2seq_hadoop.py', inputfile, '-r', 'hadoop', '--no-output',
    '-t', str(options.timesteps), '-d', options.outdir, '--variables', options.variables])

check_call(['hadoop', 'fs', '-rm', inputfile])

print 'Done!'

# Step3: Compute the global variance
    
print 'Computing the global variance...'

check_call(['time', 'python', 'mr_globalvar_hadoop.py', 
    os.path.join(options.outdir, '*/*part*.seq'),
    '-r', 'hadoop', '--no-output', '-o', os.path.join(dir, options.varname),
    '--variable', options.variables])

print 'Done!'

# Step4: Insert the global variance to a new exodus file

print 'Inserting the global variance to a new exodus file...'

check_call(['time', 'python', 'convert2exodus_download.py', 
    os.path.join(dir,options.varname,'part*'),
    '--template', options.template, '--output', options.output,
    '--tmpdir', options.tmpdir, '--varname', options.varname])

print 'Done!'

