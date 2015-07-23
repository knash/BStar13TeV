



###################################################################
##								 ##
## Name: Tagrate_Maker_B.py				         ##
## Author: Kevin Nash 						 ##
## Date: 6/5/2012						 ##
## Purpose: This program takes the root files created by  	 ##
##          TWrate.py and creates the average b-tagging rate, 	 ##
##	    then fits the average b-tagging rates		 ##
##          tagrates with a several functions 			 ##
##	    which are stored in the fitdata folder to be used    ##
##	    to weight the pre b tagged sample and create	 ##
##	    QCD background estimates				 ##
##								 ##
###################################################################

import os
import array
import glob
import math
import ROOT
import sys
from array import *
from ROOT import *
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'data',
                  dest		=	'set',
                  help		=	'data or QCD')

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'rate_default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

(options, args) = parser.parse_args()

gROOT.Macro("rootlogon.C")

import Bstar_Functions	
from Bstar_Functions import *

rootdir="rootfiles/"

setstr = ""
if options.set=='QCD':
	setstr = 'QCD'

#Make a bunch of txt files to store the fit parameters
saveout = sys.stdout

Outf1   =   open("fitdata/pol2input"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf2   =   open("fitdata/pol2input"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf4   =   open("fitdata/pol4input"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf5   =   open("fitdata/pol4input"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf7   =   open("fitdata/pol0input"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf8   =   open("fitdata/pol0input"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf10   =   open("fitdata/newfitinput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf11   =   open("fitdata/newfitinput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf13   =   open("fitdata/newfiterrorinput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf14   =   open("fitdata/newfiterrorinput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf16   =   open("fitdata/bpinput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf17   =   open("fitdata/bpinput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf19   =   open("fitdata/bperrorinput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf20   =   open("fitdata/bperrorinput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf22   =   open("fitdata/pol3input"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf23   =   open("fitdata/pol3input"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf25   =   open("fitdata/expoconinput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf26   =   open("fitdata/expoconinput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf28   =   open("fitdata/expoconerrorinput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf29   =   open("fitdata/expoconerrorinput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf31   =   open("fitdata/expolininput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf32   =   open("fitdata/expolininput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
Outf34   =   open("fitdata/expolinerrorinput"+setstr+"eta1_PSET_"+options.cuts+".txt", "w")
Outf35   =   open("fitdata/expolinerrorinput"+setstr+"eta2_PSET_"+options.cuts+".txt", "w")
sto = sys.stdout  


p0 = 0.0
p1 = 0.0
p2 = 0.0
p3 = 0.0
p4 = 0.0

p00 = 0.0
p01= 0.0
p02= 0.0
p03= 0.0
p04 = 0.0
p11= 0.0
p12= 0.0
p13= 0.0
p14 = 0.0
p22= 0.0
p23= 0.0
p24 = 0.0
p33= 0.0
p34 = 0.0
p44 = 0.0


print "Running on "+options.set

#Load up data and ttbar
fdata = TFile(rootdir+"TWratefile"+options.set+"_PSET_"+options.cuts+".root")
fttbar = TFile(rootdir+"TWratefileweightedttbar_PSET_"+options.cuts+".root")


if options.set == 'QCD' and options.cuts == 'rate_default':

	output1 = ROOT.TFile( "ModMassFile.root", "recreate" )
	output1.cd()

	ModM = fdata.Get("MpostPartial")
	ModMd = fdata.Get("Mpre")

	ModM.Rebin(40)
	ModMd.Rebin(40)

	ModM.Scale(1/ModM.Integral())
	ModMd.Scale(1/ModMd.Integral())

	ModM.Divide(ModM,ModMd,1.0,1.0,"B")

	ModM.Write("rtmass")
	output1.Close()


#Load up signal to look at contamination
#SigFiles = [
#TFile(rootdir+"TWratefileweightedsignalright800_PSET_"+options.cuts+".root"),
#TFile(rootdir+"TWratefileweightedsignalright900_PSET_"+options.cuts+".root"),
#TFile(rootdir+"TWratefileweightedsignalright1000_PSET_"+options.cuts+".root"),
#TFile(rootdir+"TWratefileweightedsignalright1100_PSET_"+options.cuts+".root"),
#TFile(rootdir+"TWratefileweightedsignalright1200_PSET_"+options.cuts+".root"),
#TFile(rootdir+"TWratefileweightedsignalright1300_PSET_"+options.cuts+".root"),
#TFile(rootdir+"TWratefileweightedsignalright1400_PSET_"+options.cuts+".root"),
#]

output = TFile( "plots/TWrate_Maker_"+setstr+"_PSET_"+options.cuts+".root", "recreate" )
output.cd()

# Get numerators and denominators for each eta region

neta1 = fdata.Get("pteta1")
deta1 = fdata.Get("pteta1pretag")

neta2 = fdata.Get("pteta2")
deta2 = fdata.Get("pteta2pretag")

# Ditto for ttbar

ttneta1 = fttbar.Get("pteta1")
ttdeta1 = fttbar.Get("pteta1pretag")

ttneta2 = fttbar.Get("pteta2")
ttdeta2 = fttbar.Get("pteta2pretag")



ntot1 = ttneta1.Integral() + neta1.Integral()
ntot2 = ttneta2.Integral() + neta2.Integral()


dtot1 = ttdeta1.Integral() + deta1.Integral()
dtot2 = ttdeta2.Integral() + deta2.Integral()

bins=[]
bins= [350,450,580,650,1000,1500,2000]
bins2=array('d',bins)

neta1r = neta1.Rebin(len(bins2)-1,"neta1r",bins2)
deta1r = deta1.Rebin(len(bins2)-1,"deta1r",bins2)

neta2r = neta2.Rebin(len(bins2)-1,"neta2r",bins2)
deta2r = deta2.Rebin(len(bins2)-1,"deta2r",bins2)

ttneta1r = ttneta1.Rebin(len(bins2)-1,"ttneta1r",bins2)
ttdeta1r = ttdeta1.Rebin(len(bins2)-1,"ttdeta1r",bins2)

ttneta2r = ttneta2.Rebin(len(bins2)-1,"ttneta2r",bins2)
ttdeta2r = ttdeta2.Rebin(len(bins2)-1,"ttdeta2r",bins2)


#TTbar subtraction is done here
if options.set=='data':
	print 'subtracting ttbar'
	neta1r.Add(ttneta1r,-1)
	deta1r.Add(ttdeta1r,-1)
	neta2r.Add(ttneta2r,-1)
	deta2r.Add(ttdeta2r,-1)


outputa = TFile( "plots/B_tagging_sigcont"+setstr+".root", "recreate" )
outputa.cd()
mass = [1300,1500,1700,1900,2100,2300,2700]
#for ifile in range(0,len(SigFiles)):
#	nseta1 = SigFiles[ifile].Get("pteta1")
#	dseta1 = SigFiles[ifile].Get("pteta1pretag")
#	nseta2 = SigFiles[ifile].Get("pteta2")
#	dseta2 = SigFiles[ifile].Get("pteta2pretag")

#	nseta1r = nseta1.Rebin(len(bins2)-1,"nseta1r",bins2)
#	dseta1r = dseta1.Rebin(len(bins2)-1,"dseta1r",bins2)

#	nseta2r = nseta2.Rebin(len(bins2)-1,"nseta2r",bins2)
#	dseta2r = dseta2.Rebin(len(bins2)-1,"dseta2r",bins2)


	
#	nseta1r.Add(neta1r)
#	dseta1r.Add(deta1r)

#	nseta2r.Add(neta2r)
#	dseta2r.Add(deta2r)

#	tagrateseta1 = nseta1r.Clone("tagrateseta1"+str(mass[ifile]))
#	tagrateseta1.Divide(tagrateseta1,dseta1r,1.0,1.0,"B")

#	tagrateseta2 = nseta2r.Clone("tagrateseta2"+str(mass[ifile]))
#	tagrateseta2.Divide(tagrateseta2,dseta2r,1.0,1.0,"B")


#	tagrateseta1.Write()
#	tagrateseta2.Write()









output.cd()

# Create subtracted tagrates by division

tagrateeta1 = neta1r.Clone("tagrateeta1")
#tagrateeta1.Divide(deta1r)
tagrateeta1.Divide(tagrateeta1,deta1r,1.0,1.0,"B")
tagrateeta2 = neta2r.Clone("tagrateeta2")
#tagrateeta2.Divide(deta2r)
tagrateeta2.Divide(tagrateeta2,deta2r,1.0,1.0,"B")



tagrateeta1.Write()
tagrateeta2.Write()


# The rest here writes the fit, and uses the covariance matrix to propagate errors for various functions

sys.stdout = saveout
print "------------------------------------"
print "POL2"
print "------------------------------------"
# This next line tells any print statement to go the the txt file Outf1
sys.stdout = Outf1
tagrateeta1.Fit("pol2","F")
fitter = TVirtualFitter.GetFitter()

for i in range(0,3):
	print(fitter.GetParameter(i))

p0 = fitter.GetCovarianceMatrixElement(0,0)
p1 = 2*fitter.GetCovarianceMatrixElement(0,1)
p2 = 2*fitter.GetCovarianceMatrixElement(0,2) + fitter.GetCovarianceMatrixElement(1,1)
p3 = 2*fitter.GetCovarianceMatrixElement(2,1)
p4 = fitter.GetCovarianceMatrixElement(2,2)

sys.stdout = Outf4
print str(p0)
print str(p1)
print str(p2)
print str(p3)
print str(p4)

sys.stdout = Outf2
tagrateeta2.Fit("pol2","F")
fitter = TVirtualFitter.GetFitter()
for i in range(0,3):
	print(fitter.GetParameter(i))

p0 = fitter.GetCovarianceMatrixElement(0,0)
p1 = 2*fitter.GetCovarianceMatrixElement(0,1)
p2 = 2*fitter.GetCovarianceMatrixElement(0,2) + fitter.GetCovarianceMatrixElement(1,1)
p3 = 2*fitter.GetCovarianceMatrixElement(2,1)
p4 = fitter.GetCovarianceMatrixElement(2,2)

sys.stdout = Outf5
print str(p0)
print str(p1)
print str(p2)
print str(p3)
print str(p4)


sys.stdout = saveout
print "------------------------------------"
print "POL0"
print "------------------------------------"
sys.stdout = Outf7
tagrateeta1.Fit("pol0","F")
fitter = TVirtualFitter.GetFitter()
print(fitter.GetParameter(0))

sys.stdout = Outf8
tagrateeta2.Fit("pol0","F")
fitter = TVirtualFitter.GetFitter()
print(fitter.GetParameter(0))


sys.stdout = saveout
print "------------------------------------"
print "BIFPOLY"
print "------------------------------------"

# This is the fit we use.  BIFP is the bifurcation point

BIFP=570.0
BP =TF1("BP",BifPoly,350,2000,5)
BP.FixParameter(4,BIFP)

c4 = TCanvas('c4', 'Tagrate1', 1300, 600)
c4.cd()
tagrateeta1.Fit("BP","F")

sys.stdout = Outf16
fitter = TVirtualFitter.GetFitter()
print(fitter.GetParameter(0))
print(fitter.GetParameter(1))
print(fitter.GetParameter(2))
print(fitter.GetParameter(3))
print(BIFP)
print BP.GetChisquare()
print BP.GetNDF()
sys.stdout = Outf19

#These constants contain info about the uncertainty from the covariance matrix
p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p33 = fitter.GetCovarianceMatrixElement(3,3)
#The funky order here is important 
print str(p00)
print str(p11)
print str(p22)
print str(p01)
print str(p02)
print str(p12)
print str(p33)
print str(p03)
print str(p13)
print(BIFP)



tagrateeta1.Draw()
c4.Print("plots/WPTAGETA1FIT"+setstr+".root","root")
c3 = TCanvas('c3', 'Tagrate2', 1300, 600)
c3.cd()

BIFP=660.0
BP =TF1("BP",BifPoly,350,2000,5)
BP.FixParameter(4,BIFP)
tagrateeta2.Fit("BP","F")
sys.stdout = saveout

sys.stdout = Outf17
fitter = TVirtualFitter.GetFitter()
print(fitter.GetParameter(0))
print(fitter.GetParameter(1))
print(fitter.GetParameter(2))
print(fitter.GetParameter(3))
print(BIFP)
print BP.GetChisquare()
print BP.GetNDF()
sys.stdout = Outf20
p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p33 = fitter.GetCovarianceMatrixElement(3,3)
print str(p00)
print str(p11)
print str(p22)
print str(p01)
print str(p02)
print str(p12)
print str(p33)
print str(p03)
print str(p13)
print(BIFP)
tagrateeta2.Draw()
c3.Print("plots/WPTAGETA2FIT"+setstr+".root","root")
#sys.exit()
#c2 = TCanvas('c2', 'Tagrate3', 1300, 600)
#c2.cd()
#fixbin = tagrateeta3.FindBin(BIFP)
#fix = tagrateeta3.GetBinContent(fixbin)
#BP.FixParameter(0,fix)

sys.stdout = saveout
print "------------------------------------"
print "POL3"
print "------------------------------------"

#c1.cd()
sys.stdout = Outf22
tagrateeta1.Fit("pol3","F")
fitter = TVirtualFitter.GetFitter()
for i in range(0,4):
	print(fitter.GetParameter(i))
#tagrateeta1.Draw()

#c2.cd()
sys.stdout = Outf23
tagrateeta2.Fit("pol3","F")
fitter = TVirtualFitter.GetFitter()
for i in range(0,4):
	print(fitter.GetParameter(i))
#tagrateeta2.Draw()


expofitlin =TF1("expofitlin","expo(0) + pol1(2)")
sys.stdout = saveout
print "------------------------------------"
print "EXPO + LINEAR"
print "------------------------------------"

#expofitlin.SetParameter(0, -1.0e+00)
#expofitlin.SetParameter(1, -7.4e-03)
#expofitlin.SetParameter(2, 4.1e-02)
#expofitlin.SetParameter(3, 4.0e-06)

#c1.cd()
sys.stdout = Outf31
tagrateeta1.Fit("expofitlin","F")
fitter = TVirtualFitter.GetFitter()
for i in range(0,4):
	print(fitter.GetParameter(i))
sys.stdout = Outf34
p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p04 = 2*fitter.GetCovarianceMatrixElement(0,4)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p14 = 2*fitter.GetCovarianceMatrixElement(1,4)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p24 = 2*fitter.GetCovarianceMatrixElement(2,4)
p33 = fitter.GetCovarianceMatrixElement(3,3)
p34 = 2*fitter.GetCovarianceMatrixElement(3,4)
p44 = fitter.GetCovarianceMatrixElement(4,4)
print str(p00)
print str(p01)
print str(p02)
print str(p03)
print str(p04)
print str(p11)
print str(p12)
print str(p13)
print str(p14)
print str(p22)
print str(p23)
print str(p24)
print str(p33)
print str(p34)
print str(p44)
#tagrateeta1.Draw()

#c2.cd()
sys.stdout = Outf32
tagrateeta2.Fit("expofitlin","F")
fitter = TVirtualFitter.GetFitter()
for i in range(0,4):
	print(fitter.GetParameter(i))
sys.stdout = Outf35
p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p04 = 2*fitter.GetCovarianceMatrixElement(0,4)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p14 = 2*fitter.GetCovarianceMatrixElement(1,4)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p24 = 2*fitter.GetCovarianceMatrixElement(2,4)
p33 = fitter.GetCovarianceMatrixElement(3,3)
p34 = 2*fitter.GetCovarianceMatrixElement(3,4)
p44 = fitter.GetCovarianceMatrixElement(4,4)
print str(p00)
print str(p01)
print str(p02)
print str(p03)
print str(p04)
print str(p11)
print str(p12)
print str(p13)
print str(p14)
print str(p22)
print str(p23)
print str(p24)
print str(p33)
print str(p34)
print str(p44)
#tagrateeta2.Draw()


sys.stdout = saveout
print "------------------------------------"
print "EXPO + CONSTANT"
print "------------------------------------"
expofit =TF1("expofit","expo(0) + pol0(2)")

#expofit.SetParameter(0, -1.03e+00);
#expofit.SetParameter(1, 0.05);
#expofit.SetParameter(2, 0.2);

#c1.cd()
sys.stdout = Outf25
tagrateeta1.Fit("expofit","F")
fitter = TVirtualFitter.GetFitter()
for i in range(0,3):
	print(fitter.GetParameter(i))
sys.stdout = Outf28
p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p33 = fitter.GetCovarianceMatrixElement(3,3)
print str(p00)
print str(p01)
print str(p02)
print str(p03)
print str(p11)
print str(p12)
print str(p13)
print str(p22)
print str(p23)
print str(p33)
#tagrateeta1.Draw()

c3.cd()
sys.stdout = Outf26
tagrateeta2.Fit("expofit","F")
fitter = TVirtualFitter.GetFitter()
for i in range(0,3):
	print(fitter.GetParameter(i))
sys.stdout = Outf29
p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p33 = fitter.GetCovarianceMatrixElement(3,3)
print str(p00)
print str(p01)
print str(p02)
print str(p03)
print str(p11)
print str(p12)
print str(p13)
print str(p22)
print str(p23)
print str(p33)
#tagrateeta2.Draw()


sys.stdout = saveout
print "------------------------------------"
print "FIT"
print "------------------------------------"
FIT =TF1("FIT","[0]*([1]+x)/([2]+x)+[3]*x")
sys.stdout = Outf10
tagrateeta1.Fit("FIT","F")
fitter = TVirtualFitter.GetFitter()
print(fitter.GetParameter(0))
print(fitter.GetParameter(1))
print(fitter.GetParameter(2))
print(fitter.GetParameter(3))

p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p33 = fitter.GetCovarianceMatrixElement(3,3)
sys.stdout = Outf13
#print_options.set_float_precision(2)
print str(p00)
print str(p01)
print str(p02)
print str(p03)
print str(p11)
print str(p12)
print str(p13)
print str(p22)
print str(p23)
print str(p33)

sys.stdout = Outf11
tagrateeta2.Fit("FIT","F")
fitter = TVirtualFitter.GetFitter()
print(fitter.GetParameter(0))
print(fitter.GetParameter(1))
print(fitter.GetParameter(2))
print(fitter.GetParameter(3))

sys.stdout = Outf14
p00 = fitter.GetCovarianceMatrixElement(0,0)
p01 = 2*fitter.GetCovarianceMatrixElement(0,1)
p02 = 2*fitter.GetCovarianceMatrixElement(0,2)
p03 = 2*fitter.GetCovarianceMatrixElement(0,3)
p11 = fitter.GetCovarianceMatrixElement(1,1)
p12 = 2*fitter.GetCovarianceMatrixElement(1,2)
p13 = 2*fitter.GetCovarianceMatrixElement(1,3)
p22 = fitter.GetCovarianceMatrixElement(2,2)
p23 = 2*fitter.GetCovarianceMatrixElement(2,3)
p33 = fitter.GetCovarianceMatrixElement(3,3)
print str(p00)
print str(p01)
print str(p02)
print str(p03)
print str(p11)
print str(p12)
print str(p13)
print str(p22)
print str(p23)
print str(p33)


#The rest of this file makes the 3d mistag rates (parameterized in pt,eta,Mtw)



output1 = ROOT.TFile( "Tagrate2D.root", "recreate" )
output2 = ROOT.TFile( "plots/Tagrate2Ddelta.root", "recreate" )

output = ROOT.TFile( "plost/TagrateSlices.root", "recreate" )

#This is one number that controls the automatic variable binning sensitivity
bres = 0.8

pre1=[]
pre2=[]	


dpre1=[]
dpre2=[]	


neta1NOSUB = fdata.Get("MtwwptcomparepostSB1e1")
deta1NOSUB = fdata.Get("MtwwptcomparepreSB1e1")

neta2NOSUB = fdata.Get("MtwwptcomparepostSB1e2")
deta2NOSUB = fdata.Get("MtwwptcomparepreSB1e2")


neta1ttbar = fttbar.Get("MtwwptcomparepostSB1e1")
deta1ttbar = fttbar.Get("MtwwptcomparepreSB1e1")

neta2ttbar = fttbar.Get("MtwwptcomparepostSB1e2")
deta2ttbar = fttbar.Get("MtwwptcomparepreSB1e2")


neta1 = neta1NOSUB.Clone("neta1")
neta1.Add(neta1ttbar,-1)

neta2 = neta2NOSUB.Clone("neta2")
neta2.Add(neta2ttbar,-1)


deta1 = deta1NOSUB.Clone("deta1")
deta1.Add(deta1ttbar,-1)

deta2 = deta2NOSUB.Clone("deta2")
deta2.Add(deta2ttbar,-1)

slopeta1 = []
slopeta2 = []


vavg1 = []
vavg2 = []


neta1r = ROOT.TH2F("neta1r",  "Comparison wpt and Mtw",   		len(bins2)-1, bins2,  140,  500,  4000 )
deta1r = ROOT.TH2F("deta1r",  "Comparison wpt and Mtw",   		len(bins2)-1, bins2,  140,  500,  4000 )

neta2r = ROOT.TH2F("neta2r",  "Comparison wpt and Mtw",   		len(bins2)-1, bins2,  140,  500,  4000 )
deta2r  = ROOT.TH2F("deta2r",  "Comparison wpt and Mtw",   		len(bins2)-1, bins2,  140,  500,  4000 )


for ibin in range(0,len(bins2)-1):

		bin1 = neta1.GetXaxis().FindBin(bins2[ibin])
		bin2 = neta1.GetXaxis().FindBin(bins2[ibin+1]-1.0)



		pre1.append(neta1.ProjectionY("SB1projYeta1_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),bin1,bin2,"e"))
		pre2.append(neta2.ProjectionY("SB1projYeta2_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),bin1,bin2,"e"))

		dpre1.append(deta1.ProjectionY("SB1projYdeta1_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),bin1,bin2,"e"))
		dpre2.append(deta2.ProjectionY("SB1projYdeta2_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),bin1,bin2,"e"))
		
		print "" 
		print bins2[ibin]
		print "THIS"
		print pre1[ibin].Integral()
		print dpre1[ibin].Integral()
		print "EQUALS"
		print neta1.Integral(bin1,bin2,0,-1)
		print deta1.Integral(bin1,bin2,0,-1)

		vavg1.append(pre1[ibin].Integral()/dpre1[ibin].Integral())
		vavg2.append(pre2[ibin].Integral()/dpre2[ibin].Integral())

		tempbin1 = 0
		error1 = ROOT.Double(1.0)

		fcont = False

		binning1= array('d',[])
		int1 = pre1[ibin].Integral()
		binning1.append(500.0)
		for ibin1 in range(1,pre1[ibin].GetNbinsX()-1):
			cont = pre1[ibin].IntegralAndError(tempbin1+1,ibin1,error1)
			if cont > 0.0:
				if not fcont:
					tempbin1 = ibin1
					binning1.append(pre1[ibin].GetBinLowEdge(tempbin1))
					fcont = True
				if error1*int1/(cont*cont) < .5:
					tempbin1 = ibin1
					binning1.append(pre1[ibin].GetBinLowEdge(tempbin1) + pre1[ibin].GetBinWidth(tempbin1))

		binning1.append(4000.0)
		print binning1
		fcont = False
		tempbin2 = 0
		error2 = ROOT.Double(1.0)

		binning2= array('d',[])
		int2 = pre2[ibin].Integral()
		binning2.append(500.0)
		for ibin2 in range(1,pre2[ibin].GetNbinsX()-1):
			cont = pre2[ibin].IntegralAndError(tempbin2+1,ibin2,error2)
			if cont > 0.0:
				if not fcont:
					tempbin2 = ibin2
					binning2.append(pre1[ibin].GetBinLowEdge(tempbin2))
					fcont = True
				if error2*int2/(cont*cont) < bres:
					tempbin2 = ibin2
					binning2.append(pre2[ibin].GetBinLowEdge(tempbin2) + pre2[ibin].GetBinWidth(tempbin2))
		binning2.append(4000.0)
		fcont = False
		tempbin3 = 0
		error3 = ROOT.Double(1.0)

		


		pre1[ibin] = pre1[ibin].Rebin(len(binning1)-1,"SB1projYeta1_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),binning1)
		pre2[ibin] = pre2[ibin].Rebin(len(binning2)-1,"SB1projYeta2_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),binning2)

		dpre1[ibin] = dpre1[ibin].Rebin(len(binning1)-1,"SB1projYdeta1_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),binning1)
		dpre2[ibin] = dpre2[ibin].Rebin(len(binning2)-1,"SB1projYdeta2_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]),binning2)
	
		for ibin1 in range(1,neta1r.GetNbinsY()):
			bcont = neta1r.GetYaxis().GetBinCenter(ibin1)

			bin1de1 = pre1[ibin].FindBin(bcont)
			bin1de2 = pre2[ibin].FindBin(bcont)
	
			neta1r.SetBinContent(ibin+1,ibin1,pre1[ibin].GetBinContent(bin1de1))
			deta1r.SetBinContent(ibin+1,ibin1,dpre1[ibin].GetBinContent(bin1de1))

			neta2r.SetBinContent(ibin+1,ibin1,pre2[ibin].GetBinContent(bin1de2))
			deta2r.SetBinContent(ibin+1,ibin1,dpre2[ibin].GetBinContent(bin1de2))


			neta1r.SetBinError(ibin+1,ibin1,pre1[ibin].GetBinError(bin1de1))
			deta1r.SetBinError(ibin+1,ibin1,dpre1[ibin].GetBinError(bin1de1))

			neta2r.SetBinError(ibin+1,ibin1,pre2[ibin].GetBinError(bin1de2))
			deta2r.SetBinError(ibin+1,ibin1,dpre2[ibin].GetBinError(bin1de2))

		pre1[ibin].Divide(pre1[ibin],dpre1[ibin],1,1,"B")
		pre2[ibin].Divide(pre2[ibin],dpre2[ibin],1,1,"B")

		pre1[ibin].Fit("pol1","F")
		fitter = TVirtualFitter.GetFitter()
		slopeta1.append(fitter.GetParameter(1))

		pre2[ibin].Fit("pol1","F")
		fitter = TVirtualFitter.GetFitter()
		slopeta2.append(fitter.GetParameter(1))



		pre1[ibin].Fit("pol0","F")
		fitter = TVirtualFitter.GetFitter()
		AVG1 = fitter.GetParameter(0)

		pre2[ibin].Fit("pol0","F")
		fitter = TVirtualFitter.GetFitter()
		AVG2 = fitter.GetParameter(0)


		pull1= pre1[ibin].Clone("PULL_SB1projYeta1_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]))
		for ibin1 in range(1,pull1.GetNbinsX()+1):
			if pull1.GetBinError(ibin1)!=0.0:
				pull1.SetBinContent(ibin1,(pull1.GetBinContent(ibin1)-AVG1)/pull1.GetBinError(ibin1))
				print (pull1.GetBinContent(ibin1)-AVG1)/pull1.GetBinError(ibin1)
			else:
				pull1.SetBinContent(ibin1,0.0)
		pull2= pre2[ibin].Clone("PULL_SB1projYeta2_"+str(bins2[ibin])+"_to_"+str(bins2[ibin+1]))
		for ibin2 in range(1,pull2.GetNbinsX()+1):
			if pull2.GetBinError(ibin2)!=0.0:
				pull2.SetBinContent(ibin2,(pull2.GetBinContent(ibin2)-AVG2)/pull2.GetBinError(ibin2))
			else:
				pull2.SetBinContent(ibin1,0.0)


		print ""

		pull1.SetFillColor(kBlue)
		pull2.SetFillColor(kBlue)

		output.cd()


tagrateeta1 = neta1r.Clone("tagrateeta1")
tagrateeta1.Divide(tagrateeta1,deta1r,1,1,"B")

tagrateeta2 = neta2r.Clone("tagrateeta2")
tagrateeta2.Divide(tagrateeta2,deta2r,1,1,"B")


output1.cd()
tagrateeta1.Write("SB1tagrate2Deta1")
tagrateeta2.Write("SB1tagrate2Deta2")

c1 = TCanvas('c1SB1', 'Pt fitted tagrate in 0.0 < Eta <0.5', 800, 500)
tagrateeta1.Draw("COLZ")
c1.RedrawAxis()
c1.Print('plots/TagrateEta1SB1'+'.root', 'root')
c1.Print('plots/TagrateEta1SB1'+'.pdf', 'pdf')
c2 = TCanvas('c2SB1', 'Pt fitted tagrate in 0.5 < Eta <1.15', 800, 500)
tagrateeta2.Draw("COLZ")
c2.RedrawAxis()
c2.Print('plots/TagrateEta2SB1'+'.root', 'root')
c2.Print('plots/TagrateEta2SB1'+'.pdf', 'pdf')
c3 = TCanvas('c3SB1', 'Pt fitted tagrate in 1.15 < Eta <2.4', 800, 500)


print vavg1
print vavg2

output1.cd()
tagrateeta1.Write()
tagrateeta2.Write()

SB2dtempeta1 = tagrateeta1.Clone("SB2dtempeta1")
SB2dtempeta2 = tagrateeta2.Clone("SB2dtempeta2")

c1 = TCanvas('c12d', 'SB2d Pt fitted tagrate in 0.0 < Eta <0.5', 800, 500)
#TGaxis.SetMaxDigits(2);
gPad.SetLeftMargin(0.12)
gPad.SetRightMargin(0.16)
#c1.SetRightMargin(0.19)
SB2dtempeta1.GetYaxis().SetTitleOffset(1.0)
SB2dtempeta2.GetZaxis().SetLabelOffset(0.1)
SB2dtempeta1.SetTitle(';Pt_{b} (GeV);M_{tb} (GeV)')
SB2dtempeta1.SetStats(0)
SB2dtempeta1.SetMaximum(0.11)
SB2dtempeta1.SetMinimum(0.0)
palette = SB2dtempeta1.GetListOfFunctions().FindObject("palette")
palette.SetX1NDC(0.85)
palette.SetX2NDC(0.9)
SB2dtempeta1.Draw("COLZ")
gPad.Update()
gPad.RedrawAxis()
c1.RedrawAxis()
c1.Print('plots/TagrateEta1SB2dSB1.root', 'root')
c1.Print('plots/TagrateEta1SB2dSB1.pdf', 'pdf')

c2 = TCanvas('c22d', 'SB2d Pt fitted tagrate in 0.5 < Eta <1.15', 800, 500)
gPad.SetLeftMargin(0.12)
gPad.SetRightMargin(0.16)
gStyle.SetPalette(1)
SB2dtempeta2.GetYaxis().SetTitleOffset(1.0)
SB2dtempeta2.GetZaxis().SetLabelOffset(0.1)
SB2dtempeta2.SetTitle(';Pt_{b} (GeV);M_{tb} (GeV)')
SB2dtempeta2.SetStats(0)
SB2dtempeta2.SetMaximum(0.11)
SB2dtempeta2.SetMinimum(0.0)
palette = SB2dtempeta2.GetListOfFunctions().FindObject("palette")
palette.SetX1NDC(0.85)
palette.SetX2NDC(0.9)
SB2dtempeta2.Draw("COLZ")
gPad.Update()
gPad.RedrawAxis()
c3.RedrawAxis()
c3.Print('plots/TagrateEta2SB2dSB1.root', 'root')
c3.Print('plots/TagrateEta2SB2dSB1.pdf', 'pdf')




output2.cd()
SBtempeta1 = tagrateeta1.Clone("SBdeltaeta1")
SBtempeta2 = tagrateeta2.Clone("SBdeltaeta2")

for xbin in range(0,SBtempeta1.GetNbinsX()+1):
			for ybin in range(0,SBtempeta1.GetNbinsY()+1):
				if SBtempeta1.GetBinContent(xbin,ybin)>0.0:
					for irange in range(0,len(bins)-1):
						#print "from " +str(bins[irange])+ " to " +str(bins[irange+1])
						#print "pt = " + str(SBtempeta1.GetXaxis().GetBinCenter(xbin))
						if bins[irange]<SBtempeta1.GetXaxis().GetBinCenter(xbin)<bins[irange+1]:
							SBtempeta1.SetBinContent(xbin,ybin,SBtempeta1.GetBinContent(xbin,ybin)-vavg1[irange])
				#else:
				#	SBtempeta1.SetBinContent(xbin,ybin,-999)

for xbin in range(0,SBtempeta2.GetNbinsX()+1):
			for ybin in range(0,SBtempeta2.GetNbinsY()+1):
				if SBtempeta2.GetBinContent(xbin,ybin)>0.0:
					for irange in range(0,len(bins)-1):
						#print "from " +str(bins[irange])+ " to " +str(bins[irange+1])
						#print "pt = " + str(SBtempeta1.GetXaxis().GetBinCenter(xbin))
						if bins[irange]<SBtempeta2.GetXaxis().GetBinCenter(xbin)<bins[irange+1]:
							SBtempeta2.SetBinContent(xbin,ybin,SBtempeta2.GetBinContent(xbin,ybin)-vavg2[irange])
				#else:
				#	SBtempeta2.SetBinContent(xbin,ybin,-999)

output2.cd()
SBtempeta1.Write()
SBtempeta2.Write()

c1 = TCanvas('c1SB1', 'SBSUB Pt fitted tagrate in 0.0 < Eta <0.5', 800, 500)
gPad.SetLeftMargin(0.16)
#gPad.SetRightMargin(0.16)
SBtempeta1.GetYaxis().SetTitleOffset(0.8)
SBtempeta1.SetTitle(';Pt_{b} (GeV);M_{tb} (GeV)')
SBtempeta1.SetStats(0)
SBtempeta1.SetMaximum(0.015)
SBtempeta1.SetMinimum(-0.015)
SBtempeta1.Draw("COLZ")
c1.RedrawAxis()
c1.Print('plots/TagrateEta1SBSUBSB1.root', 'root')
c1.Print('plots/TagrateEta1SBSUBSB1.pdf', 'pdf')
c2 = TCanvas('c2SB1', 'SBSUB Pt fitted tagrate in 0.5 < Eta <1.15', 800, 500)
gPad.SetLeftMargin(0.16)
#gPad.SetRightMargin(0.16)
SBtempeta2.GetYaxis().SetTitleOffset(0.8)
SBtempeta2.SetTitle(';Pt_{b} (GeV);M_{tb} (GeV)')
SBtempeta2.SetStats(0)
SBtempeta2.SetMaximum(0.025)
SBtempeta2.SetMinimum(-0.025)
SBtempeta2.Draw("COLZ")
c2.RedrawAxis()
c2.Print('plots/TagrateEta2SBSUBSB1.root', 'root')
c2.Print('plots/TagrateEta2SBSUBSB1.pdf', 'pdf')


