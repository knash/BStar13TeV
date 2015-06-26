
###################################################################
##								 ##
## Name: WPrime_Functions.py	   			         ##
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
import ROOT
import sys
from array import *
from ROOT import *

#This is the most impostant Function.  Correct information here is essential to obtaining valid results.
#In order we have Luminosity, top tagging scale factor, cross sections for wprime right,left,mixed,ttbar,qcd, and singletop and their corresponding event numbers
#If I wanted to access the left handed W' cross section at 1900 GeV I could do Xsecl1900 = LoadConstants()['xsec_wpl']['1900']
def LoadConstants():
	 return  {
		'lumi':19757,
		'ttagsf':1.036,
		'wtagsf':0.86,
		'xsec_wpr':{'800': 1.362,'900': 0.662,'1000': 0.336,'1100':0.178 ,'1200':0.0966 ,'1300': 0.0540,'1400': 0.0310,'1500': 0.0181,'1600': 0.0108,'1700': 0.00652,'1800': 0.00399,'1900': 0.00249,'2000': 0.00156},
		'xsec_ttbar':{'700':245.8*1.23*0.074,'1000':245.8*1.23*0.014},
		'xsec_qcd':{'300':1759.6,'470':113.9,'600':27.0,'800':3.57,'1000':0.734,'1400':0.03352235},
		'xsec_st':{'s':3.79,'sB':1.76,'t':56.4,'tB':30.7,'tW':11.1,'tWB':11.1},
		'nev_wpr':{'800':197491,'900':197117 ,'1000':196569 ,'1100':195855,'1200':195455 ,'1300':194988 ,'1400':194177 ,'1500':193291 ,'1600':193228,'1700':193362 ,'1800':192621 ,'1900':192438 ,'2000':192260},
		'nev_wpl':{'800':197537,'900':197119 ,'1000': 196274,'1100':195982,'1200': 189705,'1300': 194684,'1400':193308 ,'1500': 193758,'1600':190049,'1700': 193192,'1800':192717 ,'1900': 189458,'2000':174468},
		'nev_ttbar':{'700':3058076,'1000':1233739,'700scaleup':2225727,'1000scaleup':1225662,'700scaledown':2153111,'1000scaledown':1292980},
		'nev_qcd':{'300':5908205,'470':3919113,'600':3902030,'800':3881338,'1000':1895936,'1400':1912782},
		'nev_st':{'s':259176,'sB':139604,'t':3748155,'tB':1930185,'tW':495559,'tWB':491463},
		}

#This is also a very impostant Function.  The analysis runs on "PSETS", which correspond to the TYPE variable here.
#These each load a cut profile.  For instance 'default' is the standard selection used to set limits
def LoadCuts(TYPE):
	if TYPE=='default':
 		return  {
			'wpt':[425.0,float("inf")],
			'tpt':[425.0,float("inf")],
			'dy':[0.0,float("inf")],
			'tmass':[140.0,250.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.55],
			'tau21':[0.0,0.5],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.679,1.0],
			'wmass':[70.0,100.0],
			'eta1':[0.0,1.0],
			'eta3':[1.0,2.4]
			}
	if TYPE=='rate_default':
 		return  {
			'wpt':[425.0,float("inf")],
			'tpt':[425.0,float("inf")],
			'dy':[0.0,float("inf")],
			'tmass':[140.0,250.0],
			'nsubjets':[3,10],
			'tau32':[0.0,0.55],
			'tau21':[0.0,0.5],
			'minmass':[50.0,float("inf")],
			'sjbtag':[0.679,1.0],
			'wmass':[[30.0,70.0],[100,float("inf")]],
			'eta1':[0.0,1.0],	
			'eta3':[1.0,2.4]
			}

#This function loads up Ntuples based on what type of set you want to analyze.  
#This needs to be updated whenever new Ntuples are produced (unless the file locations are the same).
def Load_Ntuples(string):
	print 'running on ' + string 
	if string == 'data':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012A-22Jan2013/res/*.root")
		files += glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012B-22Jan2013/res/*.root")
		files += glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012C-22Jan2013/res/*.root")
		files += glob.glob("/uscms_data/d3/knash/WPrime8TeV/data/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/Run2012D-22Jan2013/res/*.root")
	if string == 'QCDHT1000':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/QCD_HT1000_to_HTinf/res/*.root" )
	if string == 'ttbar700':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/ttbar_Mtt-700to1000/res/*.root" )
	if string == 'ttbar1000':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/ttbar_Mtt-1000toinf/res/*.root" )
	if string == 'ttbar700scaleup':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/ttbar_Mtt-700to1000_scaleup/res/*.root" )
	if string == 'ttbar700scaledown':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/ttbar_Mtt-700to1000_scaledown/res/*.root" )
	if string == 'ttbar1000scaleup':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/ttbar_Mtt-1000toInf_scaleup/res/*.root")
	if string == 'ttbar1000scaledown':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/ttbar_Mtt-1000toInf_scaledown/res/*.root" )
	if string == 'singletop_s':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_s/res/*.root" )
	if string == 'singletop_sB':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_sB/res/*.root" )
	if string == 'singletop_t':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_t/res/*.root" )
	if string == 'singletop_tB':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_tB/res/*.root" )
	if string == 'singletop_tW':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_tW/res/*.root" )
	if string == 'singletop_tWB':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/singletop_tWB/res/*.root" )

	if string == 'signalright800':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-800/res/*.root" )
	if string == 'signalright900':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-900/res/*.root" )
	if string == 'signalright1000':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1000/res/*.root" )
	if string == 'signalright1100':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1100/res/*.root" )
	if string == 'signalright1200':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1200/res/*.root" )
	if string == 'signalright1300':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1300/res/*.root" )
	if string == 'signalright1400':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1400/res/*.root" )
	if string == 'signalright1500':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1500/res/*.root" )
	if string == 'signalright1600':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1600/res/*.root" )
	if string == 'signalright1700':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1700/res/*.root" )
	if string == 'signalright1800':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1800/res/*.root" )
	if string == 'signalright1900':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-1900/res/*.root" )
	if string == 'signalright2000':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_right_M-2000/res/*.root" )


	if string == 'signalleft800':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-800_left/res/*.root" )
	if string == 'signalleft900':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-900_left/res/*.root" )
	if string == 'signalleft1000':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1000_left/res/*.root" )
	if string == 'signalleft1100':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1100_left/res/*.root" )
	if string == 'signalleft1200':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1200_left/res/*.root" )
	if string == 'signalleft1300':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1300_left/res/*.root" )
	if string == 'signalleft1400':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1400/res/*.root" )
	if string == 'signalleft1500':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1500_left/res/*.root" )
	if string == 'signalleft1600':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1600/res/*.root" )
	if string == 'signalleft1700':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1700_left/res/*.root" )
	if string == 'signalleft1800':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1800/res/*.root" )
	if string == 'signalleft1900':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-1900_left/res/*.root" )
	if string == 'signalleft2000':
		files = glob.glob("/uscms_data/d3/knash/WPrime8TeV/CMSSW_5_3_18/src/Analysis/TTBSMPatTuples/test/bstar_left_M-2000/res/*.root" )

	try:
		print 'A total of ' + str(len(files)) + ' files'
	except:
		print 'Bad files option'
	return files




#This function initializes the average b tagging rates used for QCD determination
#It tages the type of functional form as an argument.  The default fit is Bifpoly

#This is a poorly written function, but I cant think of a better way to do this 
#It works, but you should be able to just have one input
def BTR_Init(ST,CUT,di):
	if ST == 'Bifpoly':
		TRBPE1 = open(di+"fitdata/bpinputeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/bpinputeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",BifPoly,0,1400,5)
		eta2fit = TF1("eta2fit",BifPoly,0,1400,5)
		Params = 5
	if ST == 'Bifpoly_err':
		TRBPE1 = open(di+"fitdata/bperrorinputeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/bperrorinputeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit=TF1("eta1fit",BifPolyErr,0,1400,10)
		eta2fit=TF1("eta2fit",BifPolyErr,0,1400,10)
		Params = 10

	if ST == 'pol0':
		TRBPE1 = open(di+"fitdata/pol0inputeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/pol0inputeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol0',0,1400)
		eta2fit = TF1("eta2fit",'pol0',0,1400)
		Params = 1

	if ST == 'pol2':
		TRBPE1 = open(di+"fitdata/pol2inputeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/pol2inputeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol2',0,1400)
		eta2fit = TF1("eta2fit",'pol2',0,1400)
		Params = 3

	if ST == 'pol3':
		TRBPE1 = open(di+"fitdata/pol3inputeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/pol3inputeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'pol3',0,1400)
		eta2fit = TF1("eta2fit",'pol3',0,1400)
		Params = 4
	if ST == 'FIT':
		TRBPE1 = open(di+"fitdata/newfitinputeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/newfitinputeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,1400)
		eta2fit = TF1("eta2fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,1400)
		Params = 4
	if ST == 'expofit':
		TRBPE1 = open(di+"fitdata/expoconinputeta1_PSET_"+CUT+".txt")
		TRBPE1.seek(0)
		TRBPE2 = open(di+"fitdata/expoconinputeta2_PSET_"+CUT+".txt")
		TRBPE2.seek(0)
		eta1fit = TF1("eta1fit",'expo(0) + pol0(2)',0,1400)
		eta2fit = TF1("eta2fit",'expo(0) + pol0(2)',0,1400)
		Params = 3

	TBP1 = TRBPE1.read()
	TBP2 = TRBPE2.read()
	
	for i in range(0,Params):

		eta1fit.SetParameter(i,float(TBP1.split('\n')[i]) )
		eta2fit.SetParameter(i,float(TBP1.split('\n')[i]) )


	return [eta1fit.Clone(),eta2fit.Clone()] 

#This takes the average b tagging rates that are initialized in the above function and produces 
#A QCD background estimate based on them 
def bkg_weight(blv, funcs, etabins):
	for ibin in range(0,len(etabins)):
		if (etabins[ibin][0] <= abs(blv.eta()) < etabins[ibin][1]) :
			tagratept = funcs[ibin].Eval(blv.pt())		
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
def Trigger_Lookup( H , TRP , TROP ):
        Weight = 1.0
        if H < 1300.0:
                bin0 = TRP.FindBin(H) 
                jetTriggerWeight = TRP.GetBinContent(bin0)
		deltaTriggerEff  = 0.5*(1.0-jetTriggerWeight)
                jetTriggerWeightUp  =   jetTriggerWeight + deltaTriggerEff
                jetTriggerWeightDown  = jetTriggerWeight - deltaTriggerEff
                jetTriggerWeightUp  = min(1.0,jetTriggerWeightUp)
                jetTriggerWeightDown  = max(0.0,jetTriggerWeightDown)
                if TROP  == "nominal" :
                	   Weight = jetTriggerWeight
                if TROP  == "up" :
                	   Weight = jetTriggerWeightUp
                if TROP == "down" :
                	   Weight = jetTriggerWeightDown
	return Weight
#This looks up the ttbar pt reweighting scale factor 
def PTW_Lookup( GP ):
		genTpt = -100.
		genTBpt = -100	
		for ig in GP :
			isT = ig.pdgId() == 6 and ig.status() == 3
			isTB = ig.pdgId() == -6 and ig.status() == 3
			if isT:
				genTpt = ig.pt()
			if isTB:
				genTBpt = ig.pt()	
		if (genTpt<0) or (genTBpt<0):
			print "ERROR"

      		wTPt = exp(0.156-0.00137*genTpt)
      		wTbarPt = exp(0.156-0.00137*genTBpt)
      		return sqrt(wTPt*wTbarPt)


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
		if FScont < 0.99:
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

