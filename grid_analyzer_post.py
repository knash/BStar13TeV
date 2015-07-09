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
                  default	=	'default',
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
wtagsf = Cons['wtagsf']
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

ttbarfiles = sorted(glob.glob('TWanalyzerttbar700*_PSET_'+cuts+'.root'))
for f in ttbarfiles:
	basename = f.replace('700','')
	name700 = f
	name1000 = f.replace('700','1000')

	scalestr = ''

	if name700.find('ttbar700scaleup') != -1:
		scalestr = 'scaleup'
	if name700.find('ttbar700scaledown') != -1:
		scalestr = 'scaledown'

	commands.append('rm ' + basename)
	commands.append('python HistoWeight.py -i '+name700+' -o temprootfiles/'+name700.replace('.root','')+'weighted.root -w ' + str(lumi*xsec_ttbar['700']*ttagsf*wtagsf/nev_ttbar['700'+scalestr]))
	commands.append('python HistoWeight.py -i '+name1000+' -o temprootfiles/'+name1000.replace('.root','')+'weighted.root -w ' + str(lumi*xsec_ttbar['1000']*ttagsf*wtagsf/nev_ttbar['1000'+scalestr]))
	commands.append('hadd '+basename+' temprootfiles/'+name700.replace('.root','')+'weighted.root temprootfiles/'+name1000.replace('.root','')+'weighted.root')
	commands.append('mv ' + name700 + ' ' + name1000 + ' temprootfiles/')
	commands.append('mv ' + basename + ' rootfiles/')


for coup in ['right','left']:
	sigfiles = sorted(glob.glob('TWanalyzersignal'+coup+'*_PSET_'+cuts+'.root'))
	for f in sigfiles:
		mass = f.replace('TWanalyzersignal'+coup,'')[:4].replace("_","")
		xsec_sig = xsec_bsr[mass]
		if coup =='right':
			nev_sig = nev_bsr[mass]
		if coup =='left':
			nev_sig = nev_bsl[mass]
	
		commands.append('rm ' + f.replace('TWanalyzersignal'+coup,'TWanalyzerweightedsignal'+coup))	 
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('TWanalyzersignal'+coup,'TWanalyzerweightedsignal'+coup)+' -w ' + str(lumi*xsec_sig*ttagsf*wtagsf/nev_sig))
		commands.append('mv '+f+' temprootfiles/')
		commands.append('mv '+f.replace('TWanalyzersignal'+coup,'TWanalyzerweightedsignal'+coup)+' rootfiles/')


stfiles = sorted(glob.glob('TWanalyzersingletop_*_Trigger_nominal_none_PSET_'+cuts+'.root'))

for f in stfiles:
	print f
	channel = f.replace('TWanalyzersingletop_','').replace('_Trigger_nominal_none_PSET_'+cuts+'.root','')
	print channel
	xsec_ST = xsec_st[channel]
	nev_ST = nev_st[channel]
	commands.append('rm ' + f.replace('TWanalyzersingletop_','TWanalyzerweightedsingletop_'))	 
	commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('TWanalyzersingletop_','TWanalyzerweightedsingletop_')+' -w ' + str(lumi*xsec_ST*ttagsf*wtagsf/nev_ST))
	commands.append('mv '+f+' temprootfiles/')
	commands.append('mv '+f.replace('TWanalyzersingletop_','TWanalyzerweightedsingletop_')+' rootfiles/')



for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )







