# !/bin/python
import subprocess
import glob
import copy
import re
import sys

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--file', metavar='F', type='string', action='store',
                  dest='file',
                  help='analysis file')


(options, args) = parser.parse_args()

argv = []

outfile = options.file.split('.')[0] 


commands = [
    'mv *.log gridpack_bsTemplate.tgz notneeded/',
    'cp ~/scripts/untarthem.py .',
    'python untarthem.py',
    'mkdir ./analysis/cache/',
    'cp ./analysis/*.cfg ./analysis/cache',
    'cp *.db ./analysis/cache',
    'cp ../' + options.file + ' ./analysis.py',
    '../utils2/theta-auto.py',
    'mkdir results',
    'mv *limit.txt results/',
    'cp analysis.py results/',
    'cp *.root results/',
    'tar -cz results/ > results_' + outfile + '.tgz'
    ]

for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

