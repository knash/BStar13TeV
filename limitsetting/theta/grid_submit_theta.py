# !/bin/python
import subprocess
import glob
import copy
import re
import sys
import os
from optparse import OptionParser


parser = OptionParser()

parser.add_option('--file', metavar='F', type='string', action='store',
                  dest='file',
                  default='analysis_wprimeR_allhad_limits.py',
                  help='analysis file')


parser.add_option('--uidir', metavar='F', type='string', action='store',
                  dest='uidir',
                  default=None,
                  help='crab UI directory')


(options, args) = parser.parse_args()

argv = []

outfile = options.file.split('.')[0] 


uidir = outfile

commands1 = []
commands2 = []
commands3 = []


commands1= [
    'rm analysis.py',
    'rm -rf analysis/',
    'rm -rf '+options.uidir,
    'rm analysis.tgz',
    'cp ' + options.file + ' ./analysis.py',
    './utils2/theta-auto.py',
    'mkdir '+options.uidir,
    'rm theta.listOfJobs'
] 
anaFilesRaw = glob.glob( 'analysis/*quant*.cfg' ) 
for ifile in range(0,len(anaFilesRaw)):
	commands2.append('echo source ./tardir/thetaGridbs.sh '+str(ifile)+' >> theta.listOfJobs')
#commands2.append('echo source ./tardir/thetaGridbs.sh 1 >> theta.listOfJaaobs')
commands2.append('cp -r theta.listOfJobs grid_theta_sub.csh analysis thetaGridbs.sh thetaGridbs.py BStarCombinationHistos_Left_Allhadronic.root BStarCombinationHistos_Left_Semileptonic.root  BStarCombinationHistos_Right_Allhadronic.root  BStarCombinationHistos_Right_Semileptonic.root  BStarCombinationHistos_Vector_Allhadronic.root  BStarCombinationHistos_Vector_Semileptonic.root  BStarCombinationHistos_Left_Dileptonic.root  BStarCombinationHistos_Right_Dileptonic.root  BStarCombinationHistos_Vector_Dileptonic.root  gridpack_bsTemplate.tgz '+options.uidir)

commands3=[
    'tar -cz ../analysis/ > ./analysis.tgz',
    'cp analysis.tgz ' + outfile + '.tgz',
    'source ./grid_theta_sub.csh'
    ]

for s in commands1 :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

for s in commands2 :
    print 'executing ' + s
    subprocess.call( [s], shell=True )
os.chdir('./'+options.uidir)
for s in commands3 :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

