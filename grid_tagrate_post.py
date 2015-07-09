#! /usr/bin/env python
import re
import os
import subprocess
from os import listdir
from os.path import isfile, join
import glob
import math
import ROOT
from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'rate_default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')
(options, args) = parser.parse_args()

cuts = options.cuts

import Bstar_Functions	
from Bstar_Functions import *

#Load up cut values based on what selection we want to run 
Cons = LoadConstants()

lumi = Cons['lumi']
ttagsf = Cons['ttagsf']
xsec_bsr = Cons['xsec_bsr']
xsec_ttbar = Cons['xsec_ttbar']
xsec_qcd = Cons['xsec_qcd']
xsec_st = Cons['xsec_st']
nev_bsr = Cons['nev_bsr']
nev_bsl = Cons['nev_bsl']
nev_ttbar = Cons['nev_ttbar']
nev_qcd = Cons['nev_qcd']
nev_st = Cons['nev_st']


files = sorted(glob.glob("*job*of*.root"))

j = []
for f in files:
	j.append(f.replace('_jo'+re.search('_jo(.+?)_PSET', f).group(1),""))

files_to_sum = list(set(j))

commands = []
commands.append('rm *.log') 
commands.append('rm temprootfiles/*.root')
commands.append('rm -rf notneeded')
for f in files_to_sum:
	commands.append('rm '+f) 
	commands.append('hadd ' + f + " " + f.replace('_PSET','_job*_PSET') )
	commands.append('mv ' +  f.replace('_PSET','_job*_PSET') + ' temprootfiles/')
	commands.append('mv ' +  f + ' rootfiles/')
commands.append('rm TWratefilettbar_PSET_'+cuts+'.root')
commands.append('python HistoWeight.py -i TWratefilettbar700_PSET_'+cuts+'.root -o temprootfiles/TWratefilettbar700_PSET_'+cuts+'weighted.root -w ' + str(lumi*xsec_ttbar['700']/nev_ttbar['700']))
commands.append('python HistoWeight.py -i TWratefilettbar1000_PSET_'+cuts+'.root -o temprootfiles/TWratefilettbar1000_PSET_'+cuts+'weighted.root -w ' + str(lumi*xsec_ttbar['1000']/nev_ttbar['1000']))
commands.append('hadd TWratefilettbar_PSET_'+cuts+'.root temprootfiles/TWratefilettbar700_PSET_'+cuts+'weighted.root temprootfiles/TWratefilettbar1000_PSET_'+cuts+'weighted.root')
commands.append('mv TWratefilettbar700_PSET_'+cuts+'.root TWratefilettbar1000_PSET_'+cuts+'.root temprootfiles/')
commands.append('mv TWratefilettbar_PSET_'+cuts+'.root rootfiles/')
for coup in ['right','left','mixed']:
	sigfiles = sorted(glob.glob('TWratefilesignal'+coup+'*_PSET_'+cuts+'.root'))
	for f in sigfiles:
		mass = f.lstrip('TWratefilesignal'+coup).rstrip('_PSET_'+cuts+'.root')
		xsec_sig = xsec_bsr[mass]
		nev_sig = nev_bsr[mass]
		commands.append('rm ' + f.replace('TWratefilesignal'+coup,'TWratefileweightedsignal'+coup))	 
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('TWratefilesignal'+coup,'TWratefileweightedsignal'+coup)+' -w ' + str(lumi*xsec_sig/nev_sig))
		commands.append('mv '+f+' temprootfiles/')
		commands.append('mv '+f.replace('TWratefilesignal'+coup,'TWratefileweightedsignal'+coup)+' rootfiles/')
for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )







