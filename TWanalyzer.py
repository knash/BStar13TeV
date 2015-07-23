#! /usr/bin/env python

###################################################################
##								 ##
## Name: TWanalyzer.py	   			                 ##
## Author: Kevin Nash 						 ##
## Date: 6/5/2012						 ##
## Purpose: This program performs the main analysis.  		 ##
##	    It takes the tagrates created by  	 		 ##
##          TWrate_Maker.py stored in fitdata, and uses 	 ##
##          them to weigh pre b tagged samples to create a 	 ##
##	    QCD background estimate along with the full event    ##
##	    selection to product Mtw inputs to Theta		 ##
##								 ##
###################################################################

import os
import glob
import math
from math import sqrt
#import quickroot
#from quickroot import *
import ROOT 
from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'data',
                  dest		=	'set',
                  help		=	'data or ttbar')
parser.add_option('-x', '--pileup', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'pileup',
                  help		=	'If not data do pileup reweighting?')
parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'num',
                  help		=	'job number')
parser.add_option('-y', '--modmass', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'modmass',
                  help		=	'nominal up or down')
parser.add_option('-j', '--jobs', metavar='F', type='string', action='store',
                  default	=	'1',
                  dest		=	'jobs',
                  help		=	'number of jobs')
parser.add_option('-t', '--tname', metavar='F', type='string', action='store',
                   default	=	'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p41_v1,HLT_PFHT900_v1',
                   dest		=	'tname',
                   help		=	'trigger name')

parser.add_option('-m', '--modulesuffix', metavar='F', type='string', action='store',
                  default	=	'none',
                  dest		=	'modulesuffix',
                  help		=	'ex. PtSmearUp')

parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                  default	=	'off',
                  dest		=	'grid',
                  help		=	'running on grid off or on')
parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default	=	'none',
                  dest		=	'ptreweight',
                  help		=	'on or off')

parser.add_option('-p', '--pdfweights', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'pdfweights',
                  help		=	'nominal, up, or down')
parser.add_option('-z', '--pdfset', metavar='F', type='string', action='store',
                  default	=	'cteq66',
                  dest		=	'pdfset',
                  help		=	'pdf set')
parser.add_option('--printEvents', metavar='F', action='store_true',
                  default=False,
                  dest='printEvents',
                  help='Print events that pass selection (run:lumi:event)')
parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

parser.add_option('-b', '--bx', metavar='F', type='string', action='store',
                   default	=	'25ns',
                   dest		=	'bx',
                   help		=	'bunch crossing 50ns or 25ns')


(options, args) = parser.parse_args()

print "Options summary"
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option]) 
	print str(opt) +': '+ str(value)
print "=================="
print ""
di = ""
if options.grid == 'on':
	di = "tardir/"
	sys.path.insert(0, 'tardir/')

gROOT.Macro(di+"rootlogon.C")

import Bstar_Functions	
from Bstar_Functions import *

tname = options.tname.split(',')
tnamestr = ''
for iname in range(0,len(tname)):
 	tnamestr+=tname[iname]
 	if iname!=len(tname)-1:
 		tnamestr+='OR'
trig='none'
if options.set!= 'data' and options.tname!='none': 
 	if options.tname=='HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p41_v1,HLT_PFHT900_v1':
 		trig = 'nominal'
 	elif options.tname!= []:
 		trig = 'tnamestr'
 		
 

#Load up cut values based on what selection we want to run 
Cuts = LoadCuts(options.cuts)
wpt = Cuts['wpt']
tpt = Cuts['tpt']
dy = Cuts['dy']
tmass = Cuts['tmass']
nsubjets = Cuts['nsubjets']
tau32 = Cuts['tau32']
tau21 = Cuts['tau21']
minmass = Cuts['minmass']
sjbtag = Cuts['sjbtag']
wmass = Cuts['wmass']
eta1 = Cuts['eta1']
eta2 = Cuts['eta2']


#For large datasets we need to parallelize the processing
jobs=int(options.jobs)
if jobs != 1:
	num=int(options.num)
	jobs=int(options.jobs)
	print "Running over " +str(jobs)+ " jobs"
	print "This will process job " +str(num)
else:
	print "Running over all events"

#This section defines some strings that are used in naming the optput files
mod = "ttbsmAna"
if options.modulesuffix != "none" :
	mod = mod + options.modulesuffix

mmstr = ""
if options.modmass!="nominal":
	print "using modm uncertainty"
	mmstr = "_modm_"+options.modmass


pstr = ""
if options.pdfweights!="nominal":
	print "using pdf uncertainty"
	pstr = "_pdf_"+options.pdfset+"_"+options.pdfweights

pustr = ""
if options.pileup=='off':
	pustr = "_pileup_unweighted"


#Based on what set we want to analyze, we find all Ntuple root files 

files = Load_Ntuples(options.set,options.bx)

if (options.set.find('ttbar') != -1) or (options.set.find('singletop') != -1):
	settype = 'ttbar'
elif (options.set.find('QCD') != -1):
	settype ='QCD'
	run_b_SF = False
else :
	
	settype = options.set.replace('right','').replace('left','')

print 'The type of set is ' + settype

ModFile = ROOT.TFile(di+"ModMassFile.root")
ModPlot = ModFile.Get("rtmass")


if options.set != 'data':
	#Load up scale factors (to be used for MC only)

	TrigFile = TFile(di+"Triggerweight_signalright2000.root")
	TrigPlot = TrigFile.Get("TriggerWeight_"+tnamestr)

	#PileFile = TFile(di+"PileUp_Ratio_"+settype+".root")
	#PilePlot = PileFile.Get("Pileup_Ratio")

# We select all the events:    
events = Events (files)

#Here we load up handles and labels.
#These are used to grab entries from the Ntuples.
#To see all the current types in an Ntuple use edmDumpEventContent /PathtoNtuple/Ntuple.root
AK8HL = Initlv("jetsAK8")

GeneratorHandle 	= 	Handle (  "GenEventInfoProduct")
GeneratorLabel  	= 	( "generator" , "")

puHandle    	= 	Handle("int")
puLabel     	= 	( "eventUserData", "puNtrueInt" )

minmassHandle 	= 	Handle (  "vector<float> "  )
minmassLabel  	= 	( "jetsAK8" , "jetAK8minmass")

nSubjetsHandle 	= 	Handle (  "vector<float> "  )
nSubjetsLabel  	= 	( "jetsAK8" , "jetAK8nSubJets")

softDropMassHandle 	= 	Handle (  "vector<float> "  )
softDropMassLabel  	= 	( "jetsAK8" , "jetAK8softDropMass")

tau1Handle 	= 	Handle (  "vector<float> "  )
tau1Label  	= 	( "jetsAK8" , "jetAK8tau1")

tau2Handle 	= 	Handle (  "vector<float> "  )
tau2Label  	= 	( "jetsAK8" , "jetAK8tau2")

tau3Handle 	= 	Handle (  "vector<float> "  )
tau3Label  	= 	( "jetsAK8" , "jetAK8tau3")

topMassHandle 	= 	Handle (  "vector<float> "  )
topMassLabel  	= 	( "jetsAK8" , "jetAK8topMass")

subjetsCSVHandle 	= 	Handle (  "vector<float> "  )
subjetsCSVLabel  	= 	( "subjetsCmsTopTag" , "subjetCmsTopTagCSV")

subjets0indexHandle 	= 	Handle (  "vector<float> "  )
subjets0indexLabel  	= 	( "jetsAK8" , "jetAK8topSubjetIndex0")

subjets1indexHandle 	= 	Handle (  "vector<float> "  )
subjets1indexLabel  	= 	( "jetsAK8" , "jetAK8topSubjetIndex1")

subjets2indexHandle 	= 	Handle (  "vector<float> "  )
subjets2indexLabel  	= 	( "jetsAK8" , "jetAK8topSubjetIndex2")

subjets3indexHandle 	= 	Handle (  "vector<float> "  )
subjets3indexLabel  	= 	( "jetsAK8" , "jetAK8topSubjetIndex3")

#---------------------------------------------------------------------------------------------------------------------#

if jobs != 1:
	f = TFile( "TWanalyzer"+options.set+"_Trigger_"+trig+"_"+options.modulesuffix +pustr+pstr+mmstr+"_job"+options.num+"of"+options.jobs+"_PSET_"+options.cuts+".root", "recreate" )
else:
	f = TFile( "TWanalyzer"+options.set+"_Trigger_"+trig+"_"+options.modulesuffix +pustr+pstr+mmstr+"_PSET_"+options.cuts+".root", "recreate" )

#Load up the average b-tagging rates -- Takes parameters from text file and makes a function
TTR = TTR_Init('Bifpoly','rate_'+options.cuts,di)
TTR_err = TTR_Init('Bifpoly_err','rate_'+options.cuts,di)
fittitles = ["pol0","pol2","pol3","FIT","Bifpoly","expofit"]
fits = []
for fittitle in fittitles:
	fits.append(TTR_Init(fittitle,'rate_'+options.cuts,di))

print "Creating histograms"

#Define Histograms

TagFile1 = TFile(di+"Tagrate2D.root")
TagPlot2de1= TagFile1.Get("tagrateeta1")
TagPlot2de2= TagFile1.Get("tagrateeta2")


f.cd()
#---------------------------------------------------------------------------------------------------------------------#
Mtw	    = TH1F("Mtw",     "mass of tw",     	  	      140, 500, 4000 )
Nevents	    = TH1F("Nevents",     	  "mass of tb",     	  	         5, 0., 5. )
QCDbkg= TH1F("QCDbkg",     "QCD background estimate",     	  	      140, 500, 4000 )
QCDbkgh= TH1F("QCDbkgh",     "QCD background estimate up error",     	  	      140, 500, 4000 )
QCDbkgl= TH1F("QCDbkgl",     "QCD background estimate down error",     	  	      140, 500, 4000 )
QCDbkg2D= TH1F("QCDbkg2D",     "QCD background estimate 2d error",     	  	      140, 500, 4000 )
QCDbkg2Dup= TH1F("QCDbkg2Dup",     "QCD background estimate 2d error",     	  	      140, 500, 4000 )
QCDbkg2Ddown= TH1F("QCDbkg2Ddown",     "QCD background estimate 2d error",     	  	      140, 500, 4000 )
Mtw.Sumw2()

QCDbkg.Sumw2()
QCDbkgh.Sumw2()
QCDbkgl.Sumw2()

QCDbkg_ARR = []

for ihist in range(0,len(fittitles)):
	QCDbkg_ARR.append(TH1F("QCDbkg"+str(fittitles[ihist]),     "mass W' in b+1 pt est etabin",     	  	      140, 500, 4000 ))
	QCDbkg_ARR[ihist].Sumw2()

#---------------------------------------------------------------------------------------------------------------------#

# loop over events
#---------------------------------------------------------------------------------------------------------------------#

count = 0
jobiter = 0
print "Start looping"
#initialize the ttree variables
tree_vars = {"wpt":array('d',[0.]),"wmass":array('d',[0.]),"tpt":array('d',[0.]),"tmass":array('d',[0.]),"tau32":array('d',[0.]),"tau21":array('d',[0.]),"nsubjets":array('d',[0.]),"sjbtag":array('d',[0.]),"weight":array('d',[0.])}
Tree = Make_Trees(tree_vars)

usegenweight = False
if options.set == "QCDFLAT7000":
	usegenweight = True
	print "Using gen weight"

goodEvents = []
totevents = events.size()
print str(totevents)  +  ' Events total'
for event in events:
    count	= 	count + 1
    m = 0
    t = 0
  #  if count > 100000:
#	break

    if count % 100000 == 0 :
      print  '--------- Processing Event ' + str(count) +'   -- percent complete ' + str(100*count/totevents) + '% -- '

    #Here we split up event processing based on number of jobs 
    #This is set up to have jobs range from 1 to the total number of jobs (ie dont start at job 0)
    if usegenweight:
		try:
			event.getByLabel (GeneratorLabel, GeneratorHandle)
    			gen 		= 	GeneratorHandle.product()
			Nevents.Fill(0.,gen.weightProduct())
		except:
			continue 
    if jobs != 1:
    	if (count - 1) % jobs == 0:
		jobiter+=1
	count_index = count - (jobiter-1)*jobs
	if count_index!=num:
		continue 
    # We load up the relevant handles and labels and create collections
    AK8LV = Makelv(AK8HL,event)
    if len(AK8LV)==0:
	continue
    tindex,windex = Hemispherize(AK8LV,AK8LV)

    wJetsh1 = []
    wJetsh0  =  []
    topJetsh1 = []
    topJetsh0  = []

    for i in range(0,len(windex[1])):
   	wJetsh1.append(AK8LV[windex[1][i]])
    for i in range(0,len(windex[0])):
    	wJetsh0.append(AK8LV[windex[0][i]])
    for i in range(0,len(tindex[1])):
    	topJetsh1.append(AK8LV[tindex[1][i]])
    for i in range(0,len(tindex[0])):
    	topJetsh0.append(AK8LV[tindex[0][i]])


    wjh0 = 0
    wjh1 = 0
    #Require 1 pt>150 jet in each hemisphere (top jets already have the 150GeV requirement) 
    for wjet in wJetsh0:
	if wjet.Perp() > 200.0:
		wjh0+=1
    for wjet in wJetsh1:
	if wjet.Perp() > 200.0:
		wjh1+=1

    njets11w0 	= 	((len(topJetsh1) == 1) and (wjh0 == 1))
    njets11w1 	= 	((len(topJetsh0) == 1) and (wjh1 == 1))
    tag = 0

  
    for hemis in ['hemis0','hemis1']:
    	if hemis == 'hemis0'   :
		if not njets11w0:
			continue 
		#The Ntuple entries are ordered in pt, so [0] is the highest pt entry
		#We are calling a candidate b jet (highest pt jet in hemisphere0)  
 		tindexval = tindex[1][0]
 		windexval = windex[0][0]

		wjet = wJetsh0[0]
		tjet = topJetsh1[0]

    	if hemis == 'hemis1'  :
		if not njets11w1:
			continue 


 		tindexval = tindex[0][0]
 		windexval = windex[1][0]

		wjet = wJetsh1[0]
		tjet = topJetsh0[0]

	if abs(wjet.Eta())>2.40 or abs(tjet.Eta())>2.40:
		continue

    	weight=1.0

    	wpt_cut = wpt[0]<wjet.Perp()<wpt[1]
    	tpt_cut = tpt[0]<tjet.Perp()<tpt[1]
    	dy_cut = dy[0]<=abs(tjet.Rapidity()-wjet.Rapidity())<dy[1]
 	if usegenweight:
 		try:
 			weight*=gen.weightProduct()
 		except:
 			continue 
    	if wpt_cut and tpt_cut and dy_cut: 

    		if options.pdfweights != "nominal" :
            		event.getByLabel( pdfLabel, pdfHandle )
            		pdfs = pdfHandle.product()
			iweight = PDF_Lookup( pdfs , options.pdfweights )
            		weight *= iweight


		if False:#options.set!="data":

			event.getByLabel (puLabel, puHandle)
    			PileUp 		= 	puHandle.product()
               		bin1 = PilePlot.FindBin(PileUp[0]) 

			if options.pileup != 'off':
				weight *= PilePlot.GetBinContent(bin1)

         	event.getByLabel (softDropMassLabel, softDropMassHandle)
         	topJetMass 	= 	softDropMassHandle.product()


		tmass_cut = tmass[0]<topJetMass[tindexval]<tmass[1]

		if tmass_cut :
	 
         		event.getByLabel ( nSubjetsLabel , nSubjetsHandle )
     			nSubjets 		= 	nSubjetsHandle.product()
         		event.getByLabel (minmassLabel, minmassHandle)
     			topJetminmass 	= 	minmassHandle.product()

			minmass_cut = minmass[0]<=topJetminmass[tindexval]<minmass[1]
			nsubjets_cut = nsubjets[0]<=nSubjets[tindexval]<nsubjets[1]


			ht = tjet.Perp() + wjet.Perp()
			if tname != 'none' and options.set!='data' :
					#Trigger reweighting done here
					TRW = Trigger_Lookup( ht , TrigPlot )
					weight*=TRW
		
			if options.ptreweight == "on":
					#ttbar pt reweighting done here
					event.getByLabel( GenLabel, GenHandle )
					GenParticles = GenHandle.product()
					PTW = PTW_Lookup( GenParticles )
					weight*=PTW
     					weightSFptup=max(0.0,weight*(2*PTW-1))
     					weightSFptdown=weight


     			event.getByLabel (subjets0indexLabel, subjets0indexHandle)
     			subjets0index 		= 	subjets0indexHandle.product() 

     			event.getByLabel (subjets1indexLabel, subjets1indexHandle)
     			subjets1index 		= 	subjets1indexHandle.product() 

     			event.getByLabel (subjets2indexLabel, subjets2indexHandle)
     			subjets2index 		= 	subjets2indexHandle.product() 

     			event.getByLabel (subjets3indexLabel, subjets3indexHandle)
     			subjets3index 		= 	subjets3indexHandle.product()
	
    		
     			event.getByLabel (subjetsCSVLabel, subjetsCSVHandle)
     			subjetsCSV 		= 	subjetsCSVHandle.product()  

 			SJ_csvs = [subjets0index,subjets1index,subjets2index,subjets3index]
 			
 			SJ_csvvals = []
 			for icsv in range(0,int(nSubjets[tindexval])):
 				if int(SJ_csvs[icsv][tindexval])!=-1:
 					SJ_csvvals.append(subjetsCSV[int(SJ_csvs[icsv][tindexval])])
 				else:
 					SJ_csvvals.append(0.)
 			SJ_csvmax = max(SJ_csvvals)
 			sjbtag_cut = sjbtag[0]<SJ_csvmax<=sjbtag[1]



     			event.getByLabel (tau3Label, tau3Handle)
     			Tau3		= 	tau3Handle.product() 
 
 
     			event.getByLabel (tau2Label, tau2Handle)
     			Tau2		= 	tau2Handle.product() 
 		
     			event.getByLabel (tau1Label, tau1Handle)
     			Tau1		= 	tau1Handle.product() 

			tau21val=Tau2[windexval]/Tau1[windexval]
			tau21_cut =  tau21[0]<=tau21val<tau21[1]

			tau32val =  Tau3[tindexval]/Tau2[tindexval]
			tau32_cut =  tau32[0]<=tau32val<tau32[1]


			wmass_cut = wmass[0]<=topJetMass[windexval]<wmass[1]

			FullTop = sjbtag_cut and tau32_cut and nsubjets_cut and minmass_cut

			if wmass_cut:
					if tau21_cut:
							eta_regions = [eta1,eta2]
							TTRweight = bkg_weight(tjet,TTR,eta_regions)
							TTRweightsigsq = bkg_weight(tjet,TTR_err,eta_regions)

							TTRweighterrup = TTRweight+sqrt(TTRweightsigsq)
							TTRweighterrdown = TTRweight-sqrt(TTRweightsigsq)


							eta1_cut = eta1[0]<=abs(tjet.Eta())<eta1[1]
							eta2_cut = eta2[0]<=abs(tjet.Eta())<eta2[1]

							modm = topJetMass[tindexval]
							if options.modmass=='nominal':
                						massw = ModPlot.Interpolate(modm)
							if options.modmass=='up':
                						massw = 1 + 0.5*(ModPlot.Interpolate(modm)-1)
							if options.modmass=='down':
                						massw = max(0.0,1 + 1.5*(ModPlot.Interpolate(modm)-1))



							if (eta1_cut) :
								xbin = TagPlot2de1.GetXaxis().FindBin(tjet.Perp())
								ybin = TagPlot2de1.GetYaxis().FindBin((tjet+wjet).M())
								tagrate2d = TagPlot2de1.GetBinContent(xbin,ybin)
								tagrate2derr = TagPlot2de1.GetBinError(xbin,ybin)
								QCDbkg2D.Fill((tjet+wjet).M(),tagrate2d*weight*massw)
								QCDbkg2Dup.Fill((tjet+wjet).M(),(tagrate2d+tagrate2derr)*weight*massw)
								QCDbkg2Ddown.Fill((tjet+wjet).M(),(tagrate2d-tagrate2derr)*weight*massw)	
			
							if (eta2_cut):
								xbin = TagPlot2de2.GetXaxis().FindBin(tjet.Perp())
								ybin = TagPlot2de2.GetYaxis().FindBin((tjet+wjet).M())
								tagrate2d = TagPlot2de2.GetBinContent(xbin,ybin)
								tagrate2derr = TagPlot2de2.GetBinError(xbin,ybin)
								QCDbkg2D.Fill((tjet+wjet).M(),tagrate2d*weight*massw)
								QCDbkg2Dup.Fill((tjet+wjet).M(),(tagrate2d+tagrate2derr)*weight*massw)
								QCDbkg2Ddown.Fill((tjet+wjet).M(),(tagrate2d-tagrate2derr)*weight*massw)	
			
							for ifit in range(0,len(fittitles)):
									tempweight = bkg_weight(tjet,fits[ifit],eta_regions)
									QCDbkg_ARR[ifit].Fill((tjet+wjet).M(),tempweight*weight*massw) 

							QCDbkg.Fill((tjet+wjet).M(),TTRweight*weight*massw)
							QCDbkgh.Fill((tjet+wjet).M(),TTRweighterrup*weight*massw)
							QCDbkgl.Fill((tjet+wjet).M(),TTRweighterrdown*weight*massw)  
        				        	if FullTop and tag==0:
                                      				goodEvents.append( [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event() ] )
								Mtw.Fill((tjet+wjet).M(),weight) 
								tag=1
								temp_variables = {"wpt":wjet.Perp(),"wmass":topJetMass[windexval],"tpt":tjet.Perp(),"tmass":topJetMass[tindexval],"tau32":tau32val,"tau21":tau21val,"nsubjets":nSubjets[tindexval],"sjbtag":SJ_csvmax,"weight":weight}

								for tv in tree_vars.keys():
									tree_vars[tv][0] = temp_variables[tv]
								Tree.Fill()
	


f.cd()
f.Write()
f.Close()

print "number of events: " + str(count)

if options.printEvents:
    Outf1   =   open("DataEvents"+options.num+".txt", "w")
    sys.stdout = Outf1
    for goodEvent in goodEvents :
        print '{0:12.0f}:{1:12.0f}:{2:12.0f}'.format(
            goodEvent[0], goodEvent[1], goodEvent[2]
        )
