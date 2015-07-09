import os
import array
import glob
import math
import ROOT
import sys
from ROOT import *
from array import *
from optparse import OptionParser
import Bstar_Functions	
from Bstar_Functions import *



bins=[500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1200,1300,1400,1500,1700,1900,2300,2700,3100]
#bins.append(3000)
bins2=array('d',bins)
print bins2


gROOT.Macro("rootlogon.C")

titles=["PtScaling","TriggerWeighting","PtSmearing"]
modsup=["ScaleUp","none","PtSmearUp"]
modsdown=["ScaleDown","none","PtSmearDown"]
trigsup=["nominal","up","nominal"]
trigsdown=["nominal","down","nominal"]

LabelsU=['__JES__','__trig__','__JER__']

#tMCentries = 6909048
#tSigma = 225.0


re=2

TTmc = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_none_PSET_default.root")

TTmcScaleUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_ScaleUp_PSET_default.root")
TTmcScaleDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_ScaleDown_PSET_default.root")

TTmcQ2ScaleUp = ROOT.TFile("rootfiles/TWanalyzerttbarscaleup_Trigger_nominal_none_PSET_default.root")
TTmcQ2ScaleDown = ROOT.TFile("rootfiles/TWanalyzerttbarscaledown_Trigger_nominal_none_PSET_default.root")


TTmcPtSmearUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_PtSmearUp_PSET_default.root")
TTmcPtSmearDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_PtSmearDown_PSET_default.root")

TTmcEtaSmearUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_EtaSmearUp_PSET_default.root")
TTmcEtaSmearDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_EtaSmearDown_PSET_default.root")

TTmcTriggerUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_up_none_PSET_default.root")
TTmcTriggerDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_down_none_PSET_default.root")

TTmcFS = TTmc.Get("Mtw")

#TTmcptup = TTmc.Get("Mtwptup")

#TTmcptdown = TTmc.Get("Mtwptdown")

TTmcQCD = TTmc.Get("QCDbkg")

TTmcQCDh = TTmc.Get("QCDbkgh")

TTmcQCDl = TTmc.Get("QCDbkgl")

TTmcFSScaleUp = TTmcScaleUp.Get("Mtw")

TTmcFSScaleDown = TTmcScaleDown.Get("Mtw")


TTmcFSQ2ScaleUp = TTmcQ2ScaleUp.Get("Mtw")
TTmcFSQ2ScaleDown = TTmcQ2ScaleDown.Get("Mtw")


TTmcFSTriggerUp = TTmcTriggerUp.Get("Mtw")

TTmcFSTriggerDown = TTmcTriggerDown.Get("Mtw")
	
TTmcFSPtSmearUp = TTmcPtSmearUp.Get("Mtw")

TTmcFSPtSmearDown = TTmcPtSmearDown.Get("Mtw")

TTmcFSEtaSmearUp = TTmcEtaSmearUp.Get("Mtw")

TTmcFSEtaSmearDown = TTmcEtaSmearDown.Get("Mtw")

Data= ROOT.TFile("rootfiles/TWanalyzerdata_Trigger_none_none_PSET_default.root")
DataMmup = ROOT.TFile("rootfiles/TWanalyzerdata_Trigger_none_none_modm_up_PSET_default.root")
DataMmdown = ROOT.TFile("rootfiles/TWanalyzerdata_Trigger_none_none_modm_down_PSET_default.root")

DataFS = Data.Get("Mtw")
DataQCDMmup = DataMmup.Get("QCDbkg")
DataQCDMmdown = DataMmdown.Get("QCDbkg")
DataQCD = Data.Get("QCDbkg")
DataQCD2d = Data.Get("QCDbkg2D")
DataQCD2dup = Data.Get("QCDbkg2Dup")
DataQCD2ddown = Data.Get("QCDbkg2Ddown")

DataQCDUp = Data.Get("QCDbkgh")
DataQCDDown = Data.Get("QCDbkgl")
TTmcQCD2d = TTmc.Get("QCDbkg2D")

DataQCD.Add(TTmcQCD,-1)
DataQCDUp.Add(TTmcQCD,-1)
DataQCDDown.Add(TTmcQCD,-1)
DataQCD2d.Add(TTmcQCD2d,-1)
DataQCD2dup.Add(TTmcQCD2d,-1)
DataQCD2ddown.Add(TTmcQCD2d,-1)
DataQCDMmup.Add(TTmcQCD,-1)
DataQCDMmdown.Add(TTmcQCD,-1)

DataQCDBEH=DataQCD.Clone("DataQCDBEH")
DataQCDBEL=DataQCD.Clone("DataQCDBEL")


DataQCD2d = DataQCD2d.Rebin(len(bins2)-1,"",bins2)
DataQCD2dup = DataQCD2dup.Rebin(len(bins2)-1,"",bins2)
DataQCD2ddown = DataQCD2ddown.Rebin(len(bins2)-1,"",bins2)
DataFS = DataFS.Rebin(len(bins2)-1,"",bins2)
DataQCD = DataQCD.Rebin(len(bins2)-1,"",bins2)
DataQCDUp = DataQCDUp.Rebin(len(bins2)-1,"",bins2)
DataQCDDown = DataQCDDown.Rebin(len(bins2)-1,"",bins2)
DataQCDBEH = DataQCDBEH.Rebin(len(bins2)-1,"",bins2)
DataQCDBEL = DataQCDBEL.Rebin(len(bins2)-1,"",bins2)
TTmcFS = TTmcFS.Rebin(len(bins2)-1,"",bins2)
DataQCDMmup = DataQCDMmup.Rebin(len(bins2)-1,"",bins2)
DataQCDMmdown = DataQCDMmdown.Rebin(len(bins2)-1,"",bins2)

TTmcFSScaleUp  = TTmcFSScaleUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSScaleDown = TTmcFSScaleDown.Rebin(len(bins2)-1,"",bins2)

TTmcFSPtSmearUp = TTmcFSPtSmearUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSPtSmearDown = TTmcFSPtSmearDown.Rebin(len(bins2)-1,"",bins2)
TTmcFSTriggerUp = TTmcFSTriggerUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSTriggerDown = TTmcFSTriggerDown.Rebin(len(bins2)-1,"",bins2)

STS = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_s_Trigger_nominal_none_PSET_default.root")
#STSScaleUp = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_s_Trigger_nominal_ScaleUp_PSET_default.root")
#STSScaleDown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_s_Trigger_nominal_ScaleDown_PSET_default.root")
#STSPtSmearUp = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_s_Trigger_nominal_PtSmearUp_PSET_default.root")
#STSPtSmearDown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_s_Trigger_nominal_PtSmearDown_PSET_default.root")
#STSTriggerup = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_s_Trigger_up_none_PSET_default.root")
#STSTriggerdown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_s_Trigger_down_none_PSET_default.root")

STSFS = STS.Get("Mtw")
STSBE = STS.Get("QCDbkg")
STSBE2d = STS.Get("QCDbkg2D")
#STSFSScaleUp = STSScaleUp.Get("Mtw")
#STSFSScaleDown = STSScaleDown.Get("Mtw")
#STSFSPtSmearUp = STSPtSmearUp.Get("Mtw")
#STSFSPtSmearDown = STSPtSmearDown.Get("Mtw")
#STSFSTriggerup = STSTriggerup.Get("Mtw")
#STSFSTriggerdown = STSTriggerdown.Get("Mtw")


STSFS = STSFS.Rebin(len(bins2)-1,"",bins2)
STSBE = STSBE.Rebin(len(bins2)-1,"",bins2)
STSBE2d = STSBE2d.Rebin(len(bins2)-1,"",bins2)
#STSFSScaleUp = STSFSScaleUp.Rebin(len(bins2)-1,"",bins2)
#STSFSScaleDown = STSFSScaleDown.Rebin(len(bins2)-1,"",bins2)
#STSFSPtSmearUp = STSFSPtSmearUp.Rebin(len(bins2)-1,"",bins2)
#STSFSPtSmearDown = STSFSPtSmearDown.Rebin(len(bins2)-1,"",bins2)
#STSFSTriggerup = STSFSTriggerup.Rebin(len(bins2)-1,"",bins2)
#STSFSTriggerdown = STSFSTriggerdown.Rebin(len(bins2)-1,"",bins2)


DataQCD.Add(STSBE,-1)
DataQCDUp.Add(STSBE,-1)
DataQCDDown.Add(STSBE,-1)
DataQCD2d.Add(STSBE2d,-1)
DataQCD2dup.Add(STSBE2d,-1)
DataQCD2ddown.Add(STSBE2d,-1)
DataQCDMmup.Add(STSBE,-1)
DataQCDMmdown.Add(STSBE,-1)

STT = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_t_Trigger_nominal_none_PSET_default.root")
#STTScaleUp = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_t_Trigger_nominal_ScaleUp_PSET_default.root")
#STTScaleDown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_t_Trigger_nominal_ScaleDown_PSET_default.root")
#STTPtSmearUp = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_t_Trigger_nominal_PtSmearUp_PSET_default.root")
#STTPtSmearDown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_t_Trigger_nominal_PtSmearDown_PSET_default.root")
#STTTriggerup = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_t_Trigger_up_none_PSET_default.root")
#STTTriggerdown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_t_Trigger_down_none_PSET_default.root")

STTFS = STT.Get("Mtw")
STTBE = STT.Get("QCDbkg")
STTBE2d = STT.Get("QCDbkg2D")
#STTFSScaleUp = STTScaleUp.Get("Mtw")
#STTFSScaleDown = STTScaleDown.Get("Mtw")
#STTFSPtSmearUp = STTPtSmearUp.Get("Mtw")
#STTFSPtSmearDown = STTPtSmearDown.Get("Mtw")
#STTFSTriggerup = STTTriggerup.Get("Mtw")
#STTFSTriggerdown = STTTriggerdown.Get("Mtw")


STTFS = STTFS.Rebin(len(bins2)-1,"",bins2)
STTBE = STTBE.Rebin(len(bins2)-1,"",bins2)
STTBE2d = STTBE2d.Rebin(len(bins2)-1,"",bins2)
#STTFSScaleUp = STTFSScaleUp.Rebin(len(bins2)-1,"",bins2)
#STTFSScaleDown = STTFSScaleDown.Rebin(len(bins2)-1,"",bins2)
#STTFSPtSmearUp = STTFSPtSmearUp.Rebin(len(bins2)-1,"",bins2)
#STTFSPtSmearDown = STTFSPtSmearDown.Rebin(len(bins2)-1,"",bins2)
#STTFSTriggerup = STTFSTriggerup.Rebin(len(bins2)-1,"",bins2)
#STTFSTriggerdown = STTFSTriggerdown.Rebin(len(bins2)-1,"",bins2)


DataQCD.Add(STTBE,-1)
DataQCDUp.Add(STTBE,-1)
DataQCDDown.Add(STTBE,-1)
DataQCD2d.Add(STTBE2d,-1)
DataQCD2dup.Add(STTBE2d,-1)
DataQCD2ddown.Add(STTBE2d,-1)
DataQCDMmup.Add(STTBE,-1)
DataQCDMmdown.Add(STTBE,-1)


STTW = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_tW_Trigger_nominal_none_PSET_default.root")
#STTWScaleUp = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_tW_Trigger_nominal_ScaleUp_PSET_default.root")
#STTWScaleDown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_tW_Trigger_nominal_ScaleDown_PSET_default.root")
#STTWPtSmearUp = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_tW_Trigger_nominal_PtSmearUp_PSET_default.root")
#STTWPtSmearDown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_tW_Trigger_nominal_PtSmearDown_PSET_default.root")
#STTWTriggerup = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_tW_Trigger_up_none_PSET_default.root")
#STTWTriggerdown = ROOT.TFile("rootfiles/TWanalyzerweightedsingletop_tW_Trigger_down_none_PSET_default.root")

STTWFS = STTW.Get("Mtw")
STTWBE = STTW.Get("QCDbkg")
STTWBE2d = STTW.Get("QCDbkg2D")
#STTWFSScaleUp = STTWScaleUp.Get("Mtw")
#STTWFSScaleDown = STTWScaleDown.Get("Mtw")
#STTWFSPtSmearUp = STTWPtSmearUp.Get("Mtw")
#STTWFSPtSmearDown = STTWPtSmearDown.Get("Mtw")
#STTWFSTriggerup = STTWTriggerup.Get("Mtw")
#STTWFSTriggerdown = STTWTriggerdown.Get("Mtw")


STTWFS = STTWFS.Rebin(len(bins2)-1,"",bins2)
STTWBE = STTWBE.Rebin(len(bins2)-1,"",bins2)
STTWBE2d = STTWBE2d.Rebin(len(bins2)-1,"",bins2)
#STTWFSScaleUp = STTWFSScaleUp.Rebin(len(bins2)-1,"",bins2)
#STTWFSScaleDown = STTWFSScaleDown.Rebin(len(bins2)-1,"",bins2)
#STTWFSPtSmearUp = STTWFSPtSmearUp.Rebin(len(bins2)-1,"",bins2)
#STTWFSPtSmearDown = STTWFSPtSmearDown.Rebin(len(bins2)-1,"",bins2)
#STTWFSTriggerup = STTWFSTriggerup.Rebin(len(bins2)-1,"",bins2)
#STTWFSTriggerdown = STTWFSTriggerdown.Rebin(len(bins2)-1,"",bins2)


DataQCD.Add(STTWBE,-1)
DataQCDUp.Add(STTWBE,-1)
DataQCDDown.Add(STTWBE,-1)
DataQCD2d.Add(STTWBE2d,-1)
DataQCD2dup.Add(STTWBE2d,-1)
DataQCD2ddown.Add(STTWBE2d,-1)
DataQCDMmup.Add(STTWBE,-1)
DataQCDMmdown.Add(STTWBE,-1)


TTmcFSQ2ScaleUp = TTmcFSQ2ScaleUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSQ2ScaleDown = TTmcFSQ2ScaleDown.Rebin(len(bins2)-1,"",bins2)



sig3d = DataQCD2dup.Clone()
sig2d = DataQCDUp.Clone()
sig3d.Add(DataQCD2d,-1)
sig2d.Add(DataQCD,-1)
extrasig = sig3d.Clone()




for ibin in range(1,sig3d.GetNbinsX()+1):
	cont3d = sig3d.GetBinContent(ibin)
	cont2d = sig2d.GetBinContent(ibin)
	newcont = sqrt(max(cont3d*cont3d-cont2d*cont2d,0.0))
	extrasig.SetBinContent(ibin,newcont)

fittitles = ["pol0","pol2","pol3","FIT","Bifpoly","expofit"]
QCDbkg_ARR = []
for ihist in range(0,len(fittitles)):
	QCDbkg_ARR.append(Data.Get("QCDbkg"+str(fittitles[ihist])))
	QCDbkg_ARR[ihist] = QCDbkg_ARR[ihist].Rebin(len(bins2)-1,"",bins2)

BEfiterrh = Fit_Uncertainty(QCDbkg_ARR)

for ibin in range(0,DataQCD.GetNbinsX()+1):

	QCDfit1=abs(DataQCDUp.GetBinContent(ibin)-DataQCD.GetBinContent(ibin))
	QCDfit2=abs(BEfiterrh.GetBinContent(ibin))
	QCDfit3=abs(DataQCD2d.GetBinContent(ibin)-DataQCD.GetBinContent(ibin))
	#QCDfit4=abs(extrasig.GetBinContent(ibin))
	QCDfit4=0.0#abs(extrasig.GetBinContent(ibin))

	QCDMm=abs((DataQCDMmup.GetBinContent(ibin)-DataQCDMmdown.GetBinContent(ibin))/2)

	QCDsys=sqrt(QCDfit1*QCDfit1+QCDfit2*QCDfit2+QCDfit3*QCDfit3+QCDfit4*QCDfit4+QCDMm*QCDMm)
	QCDerror=QCDsys

	DataQCDBEH.SetBinContent(ibin,DataQCDBEH.GetBinContent(ibin)+QCDerror)
	DataQCDBEL.SetBinContent(ibin,DataQCDBEL.GetBinContent(ibin)-QCDerror)
	print "BE Bin: "+str(DataQCDBEH.GetBinLowEdge(ibin))+" || Sigma Bin: " + str(BEfiterrh.GetBinLowEdge(ibin))
	print "Content " + str(DataQCD.GetBinContent(ibin))
	print "QCD fit error " + str(QCDfit2)
	print "QCD sidestat " + str(QCDfit1)
	print "QCD 2D error " + str(QCDfit3)
	print "Total " + str(QCDerror)



mass = [800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000]

for coup in ["right","left","vector"]:
	output = ROOT.TFile( "limitsetting/theta/BStarCombination/allhadronic"+coup+"_mtw.root", "recreate" )
	output.cd()



	DataFS.Write("mtw_allhad_type11__DATA")
	DataQCD.Write("mtw_allhad_type11__qcd")
	DataQCDBEH.Write("mtw_allhad_type11__qcd__bkg__up")
	DataQCDBEL.Write("mtw_allhad_type11__qcd__bkg__down")

	TTmcFS.Write("mtw_allhad_type11__ttbar")
	TTmcFSScaleUp.Write("mtw_allhad_type11__ttbar__JES__up")
	TTmcFSScaleDown.Write("mtw_allhad_type11__ttbar__JES__down")

	TTmcFSQ2ScaleUp.Write("mtw_allhad_type11__ttbar__Q2__up")
	TTmcFSQ2ScaleDown.Write("mtw_allhad_type11__ttbar__Q2__down")

	TTmcFSPtSmearUp.Write("mtw_allhad_type11__ttbar__JER__up")
	TTmcFSPtSmearDown.Write("mtw_allhad_type11__ttbar__JER__down")
	TTmcFSTriggerUp.Write("mtw_allhad_type11__ttbar__trig__up")
	TTmcFSTriggerDown.Write("mtw_allhad_type11__ttbar__trig__down")

	STSFS.Write("mtw_allhad_type11__sts")
	#STSFSScaleUp.Write("mtw_allhad_type11__sts__JES__up")
	#STSFSScaleDown.Write("mtw_allhad_type11__sts__JES__down")
	#STSFSPtSmearUp.Write("mtw_allhad_type11__sts__JER__up")
	#STSFSPtSmearDown.Write("mtw_allhad_type11__sts__JER__down")
	#STSFSTriggerup.Write("mtw_allhad_type11__sts__trig__up")
	#STSFSTriggerdown.Write("mtw_allhad_type11__sts__trig__down")

	STTFS.Write("mtw_allhad_type11__stt")
	#STTFSScaleUp.Write("mtw_allhad_type11__stt__JES__up")
	#STTFSScaleDown.Write("mtw_allhad_type11__stt__JES__down")
	#STTFSPtSmearUp.Write("mtw_allhad_type11__stt__JER__up")
	#STTFSPtSmearDown.Write("mtw_allhad_type11__stt__JER__down")
	#STTFSTriggerup.Write("mtw_allhad_type11__stt__trig__up")
	#STTFSTriggerdown.Write("mtw_allhad_type11__stt__trig__down")

	STTWFS.Write("mtw_allhad_type11__sttW")
	#STTWFSScaleUp.Write("mtw_allhad_type11__sttW__JES__up")
	#STTWFSScaleDown.Write("mtw_allhad_type11__sttW__JES__down")
	#STTWFSPtSmearUp.Write("mtw_allhad_type11__sttW__JER__up")
	#STTWFSPtSmearDown.Write("mtw_allhad_type11__sttW__JER__down")
	#STTWFSTriggerup.Write("mtw_allhad_type11__sttW__trig__up")
	#STTWFSTriggerdown.Write("mtw_allhad_type11__sttW__trig__down")
	for RA in range(0,len(mass)):

		SignalB11R = ROOT.TFile("rootfiles/TWanalyzerweightedsignalright"+str(mass[RA])+"_Trigger_nominal_none_PSET_default.root")
		SignalFSR = SignalB11R.Get("Mtw")
		SignalFSR = SignalFSR.Rebin(len(bins2)-1,"",bins2)

		SignalB11L = ROOT.TFile("rootfiles/TWanalyzerweightedsignalleft"+str(mass[RA])+"_Trigger_nominal_none_PSET_default.root")
		SignalFSL = SignalB11L.Get("Mtw")
		SignalFSL = SignalFSL.Rebin(len(bins2)-1,"",bins2)



		output.cd()
		if coup=="right":
			SignalFSR.Write("mtw_allhad_type11__bs"+str(mass[RA]))
		if coup=="left":
			SignalFSL.Write("mtw_allhad_type11__bs"+str(mass[RA]))
		if coup=="vector":
			SignalFSV = SignalFSR.Clone()
			SignalFSV.Add(SignalFSL)
			SignalFSV.Write("mtw_allhad_type11__bs"+str(mass[RA]))
		for i in range(0,len(modsup)):

			SignalupB11L = ROOT.TFile("rootfiles/TWanalyzerweightedsignalleft"+str(mass[RA])+"_Trigger_"+trigsup[i]+"_"+modsup[i]+"_PSET_default.root")
			SignaldownB11L = ROOT.TFile("rootfiles/TWanalyzerweightedsignalleft"+str(mass[RA])+"_Trigger_"+trigsdown[i]+"_"+modsdown[i]+"_PSET_default.root")
			SignalFSupL = SignalupB11L.Get("Mtw")
			SignalFSdownL = SignaldownB11L.Get("Mtw")
			SignalFSupL = SignalFSupL.Rebin(len(bins2)-1,"",bins2)
			SignalFSdownL = SignalFSdownL.Rebin(len(bins2)-1,"",bins2)

			SignalupB11R = ROOT.TFile("rootfiles/TWanalyzerweightedsignalright"+str(mass[RA])+"_Trigger_"+trigsup[i]+"_"+modsup[i]+"_PSET_default.root")
			SignaldownB11R = ROOT.TFile("rootfiles/TWanalyzerweightedsignalright"+str(mass[RA])+"_Trigger_"+trigsdown[i]+"_"+modsdown[i]+"_PSET_default.root")
			SignalFSupR = SignalupB11R.Get("Mtw")
			SignalFSdownR = SignaldownB11R.Get("Mtw")
			SignalFSupR = SignalFSupR.Rebin(len(bins2)-1,"",bins2)
			SignalFSdownR = SignalFSdownR.Rebin(len(bins2)-1,"",bins2)

			output.cd()


			if coup=="right":
				SignalFSdownR.Write("mtw_allhad_type11__bs"+str(mass[RA])+LabelsU[i]+"down")
				SignalFSupR.Write("mtw_allhad_type11__bs"+str(mass[RA])+LabelsU[i]+"up")
			if coup=="left":
				SignalFSdownL.Write("mtw_allhad_type11__bs"+str(mass[RA])+LabelsU[i]+"down")
				SignalFSupL.Write("mtw_allhad_type11__bs"+str(mass[RA])+LabelsU[i]+"up")
			if coup=="vector":
				SignalFSupV = SignalFSupR.Clone()
				SignalFSupV.Add(SignalFSupL)
				SignalFSupV.Write("mtw_allhad_type11__bs"+str(mass[RA])+LabelsU[i]+"up")




				SignalFSdownV = SignalFSdownR.Clone()
				SignalFSdownV.Add(SignalFSdownL)
				SignalFSdownV.Write("mtw_allhad_type11__bs"+str(mass[RA])+LabelsU[i]+"down")



	
