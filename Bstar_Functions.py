
###################################################################
##								 ##
## Name: Bstar_Functions.py	   			         ##
## Author: Kevin Nash 						 ##
## Date: 5/13/2015						 ##
## Purpose: This contains all functions used by the              ##
##	    analysis.  A method is generally placed here if 	 ##
##	    it is called more than once in reproducing all	 ##
##	    analysis results.  The functions contained here 	 ##
##	    Are capable of tuning the analysis - such as changing##
##	    cross sections, updating lumi, changing file	 ##
##	    locations, etc. with all changes propegating 	 ##
##	    to all relevant files automatically.  		 ##
##								 ##
###################################################################


import os
import array
import glob
import math
from math import sqrt
import ROOT
import sys
import cppyy
from array import *
from ROOT import *
from DataFormats.FWLite import Events, Handle
#This is the most impostant Function.  Correct information here is essential to obtaining valid results.
#In order we have Luminosity, top tagging scale factor, cross sections for wprime right,left,mixed,ttbar,qcd, and singletop and their corresponding event numbers
#If I wanted to access the left handed W' cross section at 1900 GeV I could do Xsecl1900 = LoadConstants()['xsec_wpl']['1900']
def LoadConstants():
	 return  {
		'lumi':5000.0,
		'ttagsf':1.0,
		'wtagsf':1.0,
		'xsec_bsr':{'800': 1.362,'900': 0.662,'1000': 0.336,'1100':0.178 ,'1200':0.0966 ,'1300': 0.0540,'1400': 0.0310,'1500': 0.0181,'1600': 0.0108,'1700': 0.00652,'1800': 0.00399,'1900': 0.00249,'2000': 0.00156},
		'xsec_ttbar':{'MG':806.0},
 		'xsec_qcd':{'300':7475.0,'470':587.1,'600':167.0,'800':28.25,'1000':8.195,'1400':0.7346,'800_BROKEN':32.293,'FLAT7000':2022100000},
		'xsec_st':{'s':3.79,'sB':1.76,'t':56.4,'tB':30.7,'tW':11.1,'tWB':11.1},
		'nev_bsr':{'800':197491,'900':197117 ,'1000':196569 ,'1100':195855,'1200':195455 ,'1300':194988 ,'1400':194177 ,'1500':193291 ,'1600':193228,'1700':193362 ,'1800':192621 ,'1900':192438 ,'2000':192260},
		'nev_bsl':{'800':197537,'900':197119 ,'1000': 196274,'1100':195982,'1200': 189705,'1300': 194684,'1400':193308 ,'1500': 193758,'1600':190049,'1700': 193192,'1800':192717 ,'1900': 189458,'2000':174468},
 		'nev_ttbar':{'MG':4986320},
 		'nev_qcd':{'300':2930578,'470':1939229,'600':1890256,'800':1911296,'1000':1461216,'1400':197959,'FLAT7000':209851.27},
		'nev_st':{'s':259176,'sB':139604,'t':3748155,'tB':1930185,'tW':495559,'tWB':491463},
		}

#This is also a very impostant Function.  The analysis runs on "PSETS", which correspond to the TYPE variable here.
#These each load a cut profile.  For instance 'default' is the standard selection used to set limits
def LoadCuts(TYPE):
	if TYPE=='default':
 		return  {
			'wpt':[350.0,float("inf")],
			'tpt':[350.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[130.0,200.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.61],
			'tau21':[0.0,0.5],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.890,1.0],
			'wmass':[70.0,100.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4]
			}
	if TYPE=='rate_default':
 		return  {
			'wpt':[350.0,float("inf")],
			'tpt':[350.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[130.0,200.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.61],
			'tau21':[0.0,0.5],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.890,1.0],
			'wmass':[[30.0,70.0],[100,float("inf")]],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4]
			}
	if TYPE=='sideband1':
 		return  {
			'wpt':[350.0,float("inf")],
			'tpt':[350.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[130.0,200.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.61],
			'tau21':[0.0,1.0],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.0,0.890],
			'wmass':[70.0,100.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4]
			}
	if TYPE=='rate_sideband1':
 		return  {
			'wpt':[350.0,float("inf")],
			'tpt':[350.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[130.0,200.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.61],
			'tau21':[0.0,1.0],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.0,0.890],
			'wmass':[[30.0,70.0],[100,float("inf")]],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4]
			}

	if TYPE=='sideband':
 		return  {
			'wpt':[350.0,float("inf")],
			'tpt':[350.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[130.0,200.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.61],
			'tau21':[0.5,1.0],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.890,1.0],
			'wmass':[100.0,130.0],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4]
			}
	if TYPE=='rate_sideband':
 		return  {
			'wpt':[350.0,float("inf")],
			'tpt':[350.0,float("inf")],
			'dy':[0.0,1.8],
			'tmass':[130.0,200.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.61],
			'tau21':[0.0,0.5],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.890,1.0],
			'wmass':[[30.0,70.0],[100,float("inf")]],
			'eta1':[0.0,0.8],
			'eta2':[0.8,2.4]
			}

#This function loads up Ntuples based on what type of set you want to analyze.  
#This needs to be updated whenever new Ntuples are produced (unless the file locations are the same).
def Load_Ntuples(string,bx):
	print 'running on ' + string 
	#if string == 'data':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012A-22Jan2013/res/*.root")
#		files += glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012B-22Jan2013/res/*.root")
#		files += glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012C-22Jan2013/res/*.root")
#		files += glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012D-22Jan2013/res/*.root")
 	if string == 'ttbar':
 		#files = glob.glob("/eos/uscms/store/user/srappocc/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_b2ganafw741_TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/150522_160344/0000/*.root")
 		files = glob.glob("/eos/uscms/store/user/knash/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_b2ganafw741_TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/150617_183103/0000/*.root")
 
 	if string == 'QCDPT300':
 		files = glob.glob("/eos/uscms/store/user/knash/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw741_QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/*/*/*.root")
 	if string == 'QCDPT470':
 		files = glob.glob("/eos/uscms/store/user/knash/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw741_QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/*/*/*.root")
 	if string == 'QCDPT600':
 		files = glob.glob("/eos/uscms/store/user/knash/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw741_QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/*/*/*.root")
 	if string == 'QCDPT800':
 		files = glob.glob("/eos/uscms/store/user/knash/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw741_QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/*/*/*.root")
 	if string == 'QCDPT1000':
 		files = glob.glob("/eos/uscms/store/user/knash/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw741_QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/*/*/*.root")
 	if string == 'QCDPT1400':
 		files = glob.glob("/eos/uscms/store/user/knash/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw741_QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/*/*/*.root")



	#if string == 'singletop_s':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_s/res/*.root" )
#	if string == 'singletop_sB':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_sB/res/*.root" )
#	if string == 'singletop_t':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_t/res/*.root" )
#	if string == 'singletop_tB':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_tB/res/*.root" )
#	if string == 'singletop_tW':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_tW/res/*.root" )
#	if string == 'singletop_tWB':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_tWB/res/*.root" )

#	if string == 'signalright800':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-800/res/*.root" )
#	if string == 'signalright900':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-900/res/*.root" )
#	if string == 'signalright1000':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1000/res/*.root" )
#	if string == 'signalright1100':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1100/res/*.root" )
#	if string == 'signalright1200':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1200/res/*.root" )
#	if string == 'signalright1300':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1300/res/*.root" )
#	if string == 'signalright1400':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1400/res/*.root" )
#	if string == 'signalright1500':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1500/res/*.root" )
#	if string == 'signalright1600':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1600/res/*.root" )
#	if string == 'signalright1700':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1700/res/*.root" )
#	if string == 'signalright1800':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1800/res/*.root" )
#	if string == 'signalright1900':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1900/res/*.root" )
#	if string == 'signalright2000':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-2000/res/*.root" )


#	if string == 'signalleft800':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-800/res/*.root" )
#	if string == 'signalleft900':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-900/res/*.root" )
#	if string == 'signalleft1000':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1000/res/*.root" )
#	if string == 'signalleft1100':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1100/res/*.root" )
#	if string == 'signalleft1200':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1200/res/*.root" )
#	if string == 'signalleft1300':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1300/res/*.root" )
#	if string == 'signalleft1400':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1400/res/*.root" )
#	if string == 'signalleft1500':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1500/res/*.root" )
#	if string == 'signalleft1600':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1600/res/*.root" )
#	if string == 'signalleft1700':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1700/res/*.root" )
#	if string == 'signalleft1800':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1800/res/*.root" )
#	if string == 'signalleft1900':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1900/res/*.root" )
#	if string == 'signalleft2000':
#		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-2000/res/*.root" )

	try:
		print 'A total of ' + str(len(files)) + ' files'
	except:
		print 'Bad files option'
		files = []
	return files




#This function initializes the average b tagging rates used for QCD determination
#It tages the type of functional form as an argument.  The default fit is Bifpoly

#This is a poorly written function, but I cant think of a better way to do this 
#It works, but you should be able to just have one input
def TTR_Init(ST,CUT,di):
	if ST == 'Bifpoly':
		TRBPE1 = open(di+"fitdata/bpinputQCDeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/bpinputQCDeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",BifPoly,0,2000,5)
		eta2fit = TF1("eta2fit",BifPoly,0,2000,5)
		Params = 5
	if ST == 'Bifpoly_err':
		TRBPE1 = open(di+"fitdata/bperrorinputQCDeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/bperrorinputQCDeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit=TF1("eta1fit",BifPolyErr,0,2000,10)
		eta2fit=TF1("eta2fit",BifPolyErr,0,2000,10)
		Params = 10

	if ST == 'pol0':
		TRBPE1 = open(di+"fitdata/pol0inputQCDeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/pol0inputQCDeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol0',0,2000)
		eta2fit = TF1("eta2fit",'pol0',0,2000)
		Params = 1

	if ST == 'pol2':
		TRBPE1 = open(di+"fitdata/pol2inputQCDeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/pol2inputQCDeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol2',0,2000)
		eta2fit = TF1("eta2fit",'pol2',0,2000)
		Params = 3

	if ST == 'pol3':
		TRBPE1 = open(di+"fitdata/pol3inputQCDeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/pol3inputQCDeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol3',0,2000)
		eta2fit = TF1("eta2fit",'pol3',0,2000)
		Params = 4
	if ST == 'FIT':
		TRBPE1 = open(di+"fitdata/newfitinputQCDeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/newfitinputQCDeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,2000)
		eta2fit = TF1("eta2fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,2000)
		Params = 4
	if ST == 'expofit':
		TRBPE1 = open(di+"fitdata/expoconinputQCDeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/expoconinputQCDeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'expo(0) + pol0(2)',0,2000)
		eta2fit = TF1("eta2fit",'expo(0) + pol0(2)',0,2000)
		Params = 3

	TBP1 = TRBPE1.read()
	TBP2 = TRBPE2.read()
	
	for i in range(0,Params):

		eta1fit.SetParameter(i,float(TBP1.split('\n')[i]) )
		eta2fit.SetParameter(i,float(TBP2.split('\n')[i]) )


	return [eta1fit.Clone(),eta2fit.Clone()] 

#This takes the average b tagging rates that are initialized in the above function and produces 
#A QCD background estimate based on them 
def bkg_weight(blv, funcs, etabins):
	for ibin in range(0,len(etabins)):
		if (etabins[ibin][0] <= abs(blv.Eta()) < etabins[ibin][1]) :
			tagratept = funcs[ibin].Eval(blv.Perp())		
	return tagratept

#This is the bifurcated polynomial function and its associated uncertainty 
def BifPoly( x, p ):
	xx=x[0]
	if xx<p[4]:
      		return p[0]+p[1]*xx+p[2]*(xx-p[4])**2
        else:
		return p[0]+p[1]*xx+p[3]*(xx-p[4])**2
def BifPolyErr( x, p ):
	xx=x[0]
	if xx<p[9]:
      		return p[0]+p[1]*xx**2+p[2]*(xx-p[9])**4+p[3]*xx+p[4]*(xx-p[9])**2+p[5]*xx*(xx-p[9])**2
        else:
		return p[0]+p[1]*xx**2+p[6]*(xx-p[9])**4+p[3]*xx+p[7]*(xx-p[9])**2+p[8]*xx*(xx-p[9])**2

#This looks up the PDF uncertainty
def PDF_Lookup( pdfs , pdfOP ):
	iweight = 0.0
        if pdfOP == "up" :
       		for pdf in pdfs[1::2] :
              		iweight = iweight + pdf
        else :
        	for pdf in pdfs[2::2] :
        		iweight = iweight + pdf
        return (iweight/pdfs[0]) / (len(pdfs)-1) * 2.0
#This looks up the b tagging scale factor or uncertainty
def Trigger_Lookup( H , TRP ):
        Weight = 1.0
        if H < 1300.0:
                bin0 = TRP.FindBin(H) 
                jetTriggerWeight = TRP.GetBinContent(bin0)
                Weight = jetTriggerWeight
	return Weight
#This looks up the ttbar pt reweighting scale factor 
def PTW_Lookup( GP ):
		genTpt = -100.
		genTBpt = -100	
		for ig in GP :
			isT = ig.pdgId() == 6 and ig.status() == 3
			isTB = ig.pdgId() == -6 and ig.status() == 3
			if isT:
				genTpt = ig.Perp()
			if isTB:
				genTBpt = ig.Perp()	
		if (genTpt<0) or (genTBpt<0):
			print "ERROR"

      		wTPt = exp(0.156-0.00137*genTpt)
      		wTbarPt = exp(0.156-0.00137*genTBpt)
      		return sqrt(wTPt*wTbarPt)

def Initlv(string):
 	PtHandle 	= 	Handle (  "vector<float> "  )
 	PtLabel  	= 	( string , string.replace("jets","jet")+"Pt")
 
 	EtaHandle 	= 	Handle (  "vector<float> "  )
 	EtaLabel  	= 	( string , string.replace("jets","jet")+"Eta")
 
 	PhiHandle 	= 	Handle (  "vector<float> "  )
 	PhiLabel  	= 	( string ,string.replace("jets","jet") +"Phi")
 
 	MassHandle 	= 	Handle (  "vector<float> "  )
 	MassLabel  	= 	( string ,string.replace("jets","jet") +"Mass")
 
 	return [[PtHandle,PtLabel],[EtaHandle,EtaLabel],[PhiHandle,PhiLabel],[MassHandle,MassLabel]]
 
def Makelv(vector,event):
 
     	event.getByLabel (vector[0][1], vector[0][0])
     	Pt 		= 	vector[0][0].product()
 
     	event.getByLabel (vector[1][1], vector[1][0])
     	Eta 		= 	vector[1][0].product()
 
     	event.getByLabel (vector[2][1], vector[2][0])
     	Phi 		= 	vector[2][0].product()
 
     	event.getByLabel (vector[3][1], vector[3][0])
     	Mass 		= 	vector[3][0].product()
 
 	lvs = []
 	for i in range(0,len(Pt)):
 
 		#lvs.append(ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(Pt[i],Eta[i],Phi[i],Mass[i]))
 
 		lvs.append(TLorentzVector())
 		lvs[i].SetPtEtaPhiM(Pt[i],Eta[i],Phi[i],Mass[i])
 	return lvs
 
 
def Hemispherize(LV1,LV2):
 	tjets = [[],[]]
 	wjets = [[],[]]
 	for iLV1 in range(0,len(LV1)):
 		if Math.VectorUtil.DeltaPhi(LV1[0],LV1[iLV1])> TMath.Pi()/2:
 			tjets[1].append(iLV1)
 		else:
 			tjets[0].append(iLV1)
 	for iLV2 in range(0,len(LV2)):
 		if Math.VectorUtil.DeltaPhi(LV1[0],LV2[iLV2])> TMath.Pi()/2:
 			wjets[1].append(iLV2)
 		else:
 			wjets[0].append(iLV2)
 	return tjets,wjets

#This is just a quick function to automatically make a tree
#This is used right now to automatically output branches used to validate the cuts used in a run
def Make_Trees(Floats):
        t = TTree("Tree", "Tree");
	print "Booking trees"
	for F in Floats.keys():
    		t.Branch(F, Floats[F], F+"/D")
	return t

#This takes all of the alternative fit forms for the average b tagging rate and 
#Compares them to the chosen nominal fit (bifpoly).  It outputs the mean squared error uncertainty from this comparison 
def Fit_Uncertainty(List):
	sigmah	    = List[0]
	fits=len(List)-1
	for ihist in range(0,len(List)):
		if List[ihist].GetName() == 'QCDbkgBifpoly':
			nominalhist = List[ihist]
	for ibin in range(0,nominalhist.GetXaxis().GetNbins()+1):

		mse=0.0
		sigma=0.0
		sumsqdiff = 0.0
		for ihist in range(0,len(List)):
			if List[ihist].GetName() != 'QCDbkgBifpoly':
				sumsqdiff+=(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))*(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))
		mse = sumsqdiff/fits
		sigma = sqrt(mse)
		sigmah.SetBinContent(ibin,sigma)
	
	return sigmah

#Makes the blue pull plots
def Make_Pull_plot( DATA,BKG,BKGUP,BKGDOWN ):
	pull = DATA.Clone("pull")
	pull.Add(BKG,-1)
	sigma = 0.0
	FScont = 0.0
	BKGcont = 0.0
	for ibin in range(1,pull.GetNbinsX()+1):
		FScont = DATA.GetBinContent(ibin)
		BKGcont = BKG.GetBinContent(ibin)
		if FScont>=BKGcont:
			FSerr = DATA.GetBinErrorLow(ibin)
			BKGerr = abs(BKGUP.GetBinContent(ibin)-BKG.GetBinContent(ibin))
		if FScont<BKGcont:
			FSerr = DATA.GetBinErrorUp(ibin)
			BKGerr = abs(BKGDOWN.GetBinContent(ibin)-BKG.GetBinContent(ibin))
		sigma = sqrt(FSerr*FSerr + BKGerr*BKGerr)
		if FScont == 0.0:
			pull.SetBinContent(ibin, 0.0 )	
		else:
			if sigma != 0 :
				pullcont = (pull.GetBinContent(ibin))/sigma
				pull.SetBinContent(ibin, pullcont)
			else :
				pull.SetBinContent(ibin, 0.0 )
	return pull
#Some lazy string formatting functions 
def strf( x ):
	return '%.2f' % x

def strf1( x ):
	return '%.0f' % x

