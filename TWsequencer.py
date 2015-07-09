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
parser.add_option('-c', '--command', metavar='F', type='string', action='store',
                  default	=	'',
                  dest		=	'command',
                  help		=	'command to run on signal')
(options, args) = parser.parse_args()

sigpoints = ['800','900','1000','1100','1200','1300','1400','1500','1600','1700','1800','1900','2000']

for j in sigpoints:
    	print 'executing ' + options.command.replace('signalright','signalright'+j).replace('signalleft','signalleft'+j).replace('_',' ')
    	subprocess.call( [options.command.replace('signalright','signalright'+j).replace('signalleft','signalleft'+j).replace('_',' ')], shell=True )







