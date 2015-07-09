

import os
import array
import glob
import math
import ROOT
import sys
from ROOT import *
from array import *
from optparse import OptionParser
gROOT.Macro("rootlogon.C")
gROOT.LoadMacro("insertlogo.C+")
parser = OptionParser()

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')
(options, args) = parser.parse_args()

cuts = options.cuts


import Bstar_Functions	
from Bstar_Functions import *

st1= ROOT.THStack("st1", "st1")

leg = TLegend(0.45, 0.35, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

leg1 = TLegend(0.45, 0.5, 0.84, 0.84)
leg1.SetFillColor(0)
leg1.SetBorderSize(0)


leg2 = TLegend(0.5, 0.5, 0.84, 0.84)
leg2.SetFillColor(0)
leg2.SetBorderSize(0)

rebin =4


bins=[500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1200,1300,1400,1500,1700,1900,2300,2700,3100]
#bins.append(3000)
bins2=array('d',bins)

Mult = 1.0

#Kfac=1.2



sigf = [
ROOT.TFile("rootfiles/TWanalyzerweightedsignalright1200_Trigger_nominal_none_PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/TWanalyzerweightedsignalright1500_Trigger_nominal_none_PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/TWanalyzerweightedsignalright1800_Trigger_nominal_none_PSET_"+options.cuts+".root")
]

sigh = [
sigf[0].Get("Mtw"),
sigf[1].Get("Mtw"),
sigf[2].Get("Mtw")
]

sigh[0].Scale(Mult)
sigh[1].Scale(Mult)
sigh[2].Scale(Mult)

sigh[0] = sigh[0].Rebin(len(bins2)-1,"",bins2)
sigh[1] = sigh[1].Rebin(len(bins2)-1,"",bins2)
sigh[2] = sigh[2].Rebin(len(bins2)-1,"",bins2)

sigh[0].SetLineStyle(5)
sigh[1].SetLineStyle(6)
sigh[2].SetLineStyle(7)

sigh[0].SetLineWidth(2)
sigh[1].SetLineWidth(2)
sigh[2].SetLineWidth(2)

sigh[0].SetLineColor(1)
sigh[1].SetLineColor(2)
sigh[2].SetLineColor(4)

stops = ['singletop_s','singletop_sB','singletop_t','singletop_tB','singletop_tW','singletop_tWB']

sfiles=[]
shists=[]
ssubs=[]
ssubsh=[]
ssubsl=[]


Data = ROOT.TFile("rootfiles/TWanalyzerdata_Trigger_none_none_PSET_"+options.cuts+".root")
DataMmup = ROOT.TFile("rootfiles/TWanalyzerdata_Trigger_none_none_modm_up_PSET_default.root")
DataMmdown = ROOT.TFile("rootfiles/TWanalyzerdata_Trigger_none_none_modm_down_PSET_default.root")

DataFS = Data.Get("Mtw")
DataBE = Data.Get("QCDbkg")

DataBE2d = Data.Get("QCDbkg2D")
DataBEMmup = DataMmup.Get("QCDbkg")
DataBEMmdown = DataMmdown.Get("QCDbkg")
DataBE2dup = Data.Get("QCDbkg2Dup")
DataBE2ddown = Data.Get("QCDbkg2Ddown")

c1 = TCanvas('c1', 'Data Full selection vs b pt tagging background', 700, 600)

main = ROOT.TPad("main", "main", 0, 0.3, 1, 1)
sub = ROOT.TPad("sub", "sub", 0, 0, 1, 0.3)

main.SetLeftMargin(0.16)
main.SetRightMargin(0.05)
main.SetTopMargin(0.11)
main.SetBottomMargin(0.0)

sub.SetLeftMargin(0.16)
sub.SetRightMargin(0.05)
sub.SetTopMargin(0)
sub.SetBottomMargin(0.3)

main.Draw()
sub.Draw()

main.cd()

TTmc = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_none_PSET_"+options.cuts+".root")


TTmcScaleUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_ScaleUp_PSET_"+options.cuts+".root")
TTmcScaleDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_ScaleDown_PSET_"+options.cuts+".root")

TTmcPtSmearUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_PtSmearUp_PSET_"+options.cuts+".root")
TTmcPtSmearDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_PtSmearDown_PSET_"+options.cuts+".root")

TTmcQ2ScaleUp = ROOT.TFile("rootfiles/TWanalyzerttbarscaleup_Trigger_nominal_none_PSET_"+options.cuts+".root")
TTmcQ2ScaleDown = ROOT.TFile("rootfiles/TWanalyzerttbarscaledown_Trigger_nominal_none_PSET_"+options.cuts+".root")




TTmcEtaSmearUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_EtaSmearUp_PSET_"+options.cuts+".root")
TTmcEtaSmearDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_nominal_EtaSmearDown_PSET_"+options.cuts+".root")

TTmcTriggerUp = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_up_none_PSET_"+options.cuts+".root")
TTmcTriggerDown = ROOT.TFile("rootfiles/TWanalyzerttbar_Trigger_down_none_PSET_"+options.cuts+".root")

output = ROOT.TFile( "TWanalyzer_output_PSET_"+options.cuts+".root", "recreate" )
output.cd()

TTmcFS = TTmc.Get("Mtw")

TTmcBE = TTmc.Get("QCDbkg")

TTmcBE2d = TTmc.Get("QCDbkg2D")


TTmcBEh = TTmc.Get("QCDbkgh")
DataBEh = Data.Get("QCDbkgh")

TTmcBEl = TTmc.Get("QCDbkgl")
DataBEl = Data.Get("QCDbkgl")

TTmcFSScaleUp = TTmcScaleUp.Get("Mtw")
TTmcFSScaleDown = TTmcScaleDown.Get("Mtw")

TTmcFSQ2ScaleUp = TTmcQ2ScaleUp.Get("Mtw")
TTmcFSQ2ScaleDown = TTmcQ2ScaleDown.Get("Mtw")

TTmcFSPtSmearUp = TTmcPtSmearUp.Get("Mtw")
TTmcFSPtSmearDown = TTmcPtSmearDown.Get("Mtw")

TTmcFSEtaSmearUp = TTmcEtaSmearUp.Get("Mtw")
TTmcFSEtaSmearDown = TTmcEtaSmearDown.Get("Mtw")

TTmcFSTriggerUp = TTmcTriggerUp.Get("Mtw")
TTmcFSTriggerDown = TTmcTriggerDown.Get("Mtw")

DataBEMmup = DataBEMmup.Rebin(len(bins2)-1,"",bins2)
DataBEMmdown = DataBEMmdown.Rebin(len(bins2)-1,"",bins2)

DataBE2dup = DataBE2dup.Rebin(len(bins2)-1,"",bins2)
DataBE2ddown = DataBE2ddown.Rebin(len(bins2)-1,"",bins2)

TTmcFSQ2ScaleUp = TTmcFSQ2ScaleUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSQ2ScaleDown = TTmcFSQ2ScaleDown.Rebin(len(bins2)-1,"",bins2)

TTmcFSScaleUp = TTmcFSScaleUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSScaleDown =  TTmcFSScaleDown.Rebin(len(bins2)-1,"",bins2)

TTmcFSPtSmearUp =  TTmcFSPtSmearUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSPtSmearDown =  TTmcFSPtSmearDown.Rebin(len(bins2)-1,"",bins2)

TTmcFSEtaSmearUp = TTmcFSEtaSmearUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSEtaSmearDown = TTmcFSEtaSmearDown.Rebin(len(bins2)-1,"",bins2)

TTmcFSTriggerUp = TTmcFSTriggerUp.Rebin(len(bins2)-1,"",bins2)
TTmcFSTriggerDown = TTmcFSTriggerDown.Rebin(len(bins2)-1,"",bins2)


DataBE2d = DataBE2d.Rebin(len(bins2)-1,"",bins2)
TTmcFS = TTmcFS.Rebin(len(bins2)-1,"",bins2)
DataBE = DataBE.Rebin(len(bins2)-1,"",bins2)
DataFS = DataFS.Rebin(len(bins2)-1,"",bins2)
print DataFS.Integral()
DataBEl = DataBEl.Rebin(len(bins2)-1,"",bins2)
DataBEh = DataBEh.Rebin(len(bins2)-1,"",bins2)
TTmcBE = TTmcBE.Rebin(len(bins2)-1,"",bins2)
TTmcBE2d = TTmcBE2d.Rebin(len(bins2)-1,"",bins2)
TTmcBEh = TTmcBEh.Rebin(len(bins2)-1,"",bins2)
TTmcBEl = TTmcBEl.Rebin(len(bins2)-1,"",bins2)

#subtract weighted TT pretags

unsubbkg = DataBE.Clone()

DataBE.Add(TTmcBE,-1)
DataBE2d.Add(TTmcBE2d,-1)
DataBE2dup.Add(TTmcBE2d,-1)
DataBE2ddown.Add(TTmcBE2d,-1)
DataBEl.Add(TTmcBE,-1)
DataBEh.Add(TTmcBE,-1)
DataBEMmup.Add(TTmcBE,-1)
DataBEMmdown.Add(TTmcBE,-1)


singletop = ROOT.TH1F("singletop",     "singletop",     	  	      140, 500, 4000 )
singletop = singletop.Rebin(len(bins2)-1,"",bins2)

schanst = ROOT.TH1F("schanst",     "singletop",     	  	      140, 500, 4000 )
schanst = schanst.Rebin(len(bins2)-1,"",bins2)
for ifile in range(0,len(stops)):
	sfiles.append(ROOT.TFile("rootfiles/TWanalyzerweighted"+stops[ifile]+"_Trigger_nominal_none_PSET_"+options.cuts+".root"))
	shists.append(sfiles[ifile].Get("Mtw"))
	ssubs.append(sfiles[ifile].Get("QCDbkg"))

	ssubsh.append(sfiles[ifile].Get("QCDbkgh"))
	ssubsl.append(sfiles[ifile].Get("QCDbkgl"))
	shists[ifile] = shists[ifile].Rebin(len(bins2)-1,"",bins2)
	ssubs[ifile] = ssubs[ifile].Rebin(len(bins2)-1,"",bins2)
	ssubsh[ifile] = ssubsh[ifile].Rebin(len(bins2)-1,"",bins2)
	ssubsl[ifile] = ssubsl[ifile].Rebin(len(bins2)-1,"",bins2)
	#print str((Luminosity*stopxsecs[ifile]*TeffScale)/stopnevents[ifile])    
	DataBE.Add(ssubs[ifile],-1)
	DataBEl.Add(ssubsl[ifile],-1)
	DataBEh.Add(ssubsh[ifile],-1)  
	singletop.SetFillColor(6)
	singletop.Add(shists[ifile])
	if ifile<=1:
		schanst.Add(shists[ifile])

st1.Add(singletop)

output.cd()

fittitles = ["pol0","pol2","pol3","FIT","Bifpoly","expofit"]
QCDbkg_ARR = []
for ihist in range(0,len(fittitles)):
	QCDbkg_ARR.append(Data.Get("QCDbkg"+str(fittitles[ihist])))
	QCDbkg_ARR[ihist] = QCDbkg_ARR[ihist].Rebin(len(bins2)-1,"",bins2)

BEfiterrh = Fit_Uncertainty(QCDbkg_ARR)

sig3d = DataBE2dup.Clone()
sig2d = DataBEh.Clone()
sig3d.Add(DataBE2d,-1)
sig2d.Add(DataBE,-1)
extrasig = sig3d.Clone()




for ibin in range(1,sig3d.GetNbinsX()+1):
	cont3d = sig3d.GetBinContent(ibin)
	cont2d = sig2d.GetBinContent(ibin)
	newcont = sqrt(max(cont3d*cont3d-cont2d*cont2d,0.0))
	extrasig.SetBinContent(ibin,newcont)


output.cd()
DataQCDBEH=DataBE.Clone("DataQCDBEH")
DataQCDBEL=DataBE.Clone("DataQCDBEL")
DataTOTALBEH=DataBE.Clone("DataTOTALBEH")
DataTOTALBEL=DataBE.Clone("DataTOTALBEL")

for ibin in range(0,DataBE.GetNbinsX()):
	PtScaleup=(TTmcFSScaleUp.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	Q2Scaleup=(TTmcFSQ2ScaleUp.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	PtSmearup=(TTmcFSPtSmearUp.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	EtaSmearup=(TTmcFSEtaSmearUp.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	Triggerup=(TTmcFSTriggerUp.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))


	PtScaledown=(TTmcFSScaleDown.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	Q2Scaledown=(TTmcFSQ2ScaleDown.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	PtSmeardown=(TTmcFSPtSmearDown.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	EtaSmeardown=(TTmcFSEtaSmearDown.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))
	Triggerdown=(TTmcFSTriggerDown.GetBinContent(ibin) -TTmcFS.GetBinContent(ibin))

	ups = [PtScaleup,Q2Scaleup,PtSmearup,EtaSmearup,Triggerup]
	downs = [PtScaledown,Q2Scaledown,PtSmeardown,EtaSmeardown,Triggerdown]
	
	upstr = ["PtScaleup","Q2Scaleup","PtSmearup","EtaSmearup","Triggerup"]
	downstr = ["PtScaledown","Q2Scaledown","PtSmeardown","EtaSmeardown","Triggerdown"]

	sigsqup = 0.
	sigsqdown = 0.

	for i in range(0,len(ups)):
		upsig = max(ups[i],downs[i],0.)
		downsig = min(ups[i],downs[i],0.)
		sigsqup+=upsig*upsig
		sigsqdown+=downsig*downsig

	CrossSection=0.22*TTmcFS.GetBinContent(ibin)
	TTstat=TTmcFS.GetBinError(ibin)
	if DataBE.GetBinContent(ibin)>0:
		QCDstat=DataBE.GetBinError(ibin)
	else:
		QCDstat=0.
	QCDfit=abs(BEfiterrh.GetBinContent(ibin))
	QCDfit1=abs((DataBEh.GetBinContent(ibin)-DataBEl.GetBinContent(ibin))/2)
	QCDfit2=abs(DataBE2d.GetBinContent(ibin)-DataBE.GetBinContent(ibin))
	QCDfit3=abs(extrasig.GetBinContent(ibin))
	QCDMm=abs((DataBEMmup.GetBinContent(ibin)-DataBEMmdown.GetBinContent(ibin))/2)


	QCDsys=sqrt(QCDfit*QCDfit + QCDfit1*QCDfit1 + QCDfit2*QCDfit2+ QCDfit3*QCDfit3+QCDMm*QCDMm)
	QCDerror= sqrt(QCDstat*QCDstat+QCDsys*QCDsys)
	TTerrorup=sqrt(sigsqup+TTstat*TTstat+CrossSection*CrossSection)
	TTerrordown=sqrt(sigsqdown+TTstat*TTstat+CrossSection*CrossSection)
	Totalerrorup=sqrt(QCDerror*QCDerror+TTerrorup*TTerrorup)
	Totalerrordown=sqrt(QCDerror*QCDerror+TTerrordown*TTerrordown)
	DataQCDBEH.SetBinContent(ibin,DataQCDBEH.GetBinContent(ibin)+QCDerror)
	DataQCDBEL.SetBinContent(ibin,DataQCDBEL.GetBinContent(ibin)-QCDerror)
	DataTOTALBEH.SetBinContent(ibin,DataTOTALBEH.GetBinContent(ibin)+Totalerrorup)
	DataTOTALBEL.SetBinContent(ibin,DataTOTALBEL.GetBinContent(ibin)-Totalerrordown)
print "QCD total error"
print (DataQCDBEH.Integral()-DataBE.Integral())/DataBE.Integral()
print 
DataQCDBEH.Write()
DataQCDBEL.Write()

DataTOTALBEH.Write()
DataTOTALBEL.Write()

DataTOTALBEL.Add(TTmcFS)
DataTOTALBEH.Add(TTmcFS)
#DataTOTALBEL.Add(singletop)
#DataTOTALBEH.Add(singletop)

for ifile in range(0,len(stops)):
	DataTOTALBEL.Add(shists[ifile])
	DataTOTALBEH.Add(shists[ifile])		

DataBE.SetFillColor(TROOT.kYellow)
TTmcFS.SetFillColor(TROOT.kRed)

DataTOTALBEH.SetLineColor(kBlue)
DataTOTALBEH.SetLineWidth(2)
#DataTOTALBEH.SetLineStyle(2)

centerqcd = DataTOTALBEL.Clone("centerqcd")
centerqcd.SetFillColor(TROOT.kYellow)
centerqcd.Add(TTmcFS,-1)
centerqcd.Add(singletop,-1)

DataTOTALBEL.SetLineColor(kBlue)
DataTOTALBEL.SetLineWidth(2)
#DataTOTALBEL.SetFillColor(0)
#DataTOTALBEL.SetLineStyle(0)
#DataTOTALBEL.SetLineWidth(2)
#DataTOTALBEL.SetLineStyle(2)

sigst= ROOT.THStack("sigst", "sigst")
sigma = DataTOTALBEH.Clone("sigma")
sigma.SetFillStyle(3245)
sigma.SetFillColor(1)
sigma.SetLineColor(0)
centerqcd.SetLineColor(TROOT.kYellow)

sigma.Add(DataTOTALBEL,-1)
sigst.Add(singletop)
sigst.Add(TTmcFS)
sigst.Add(centerqcd)
sigst.Add(sigma)


st1.Add(TTmcFS)
st1.Add(DataBE)

bkgline=st1.GetStack().Last().Clone("bkgline")
bkgline.SetFillColor(0)
bkgline.SetFillStyle(0)

leg.AddEntry( DataFS, 'Data', 'P')
leg.AddEntry( DataBE, 'QCD background prediction', 'F')
leg.AddEntry( TTmcFS, 't#bar{t} MC prediction', 'F')
leg.AddEntry( singletop, 'Single top quark MC prediction', 'F')
leg.AddEntry( sigma, '1 #sigma background uncertainty', 'F')
leg.AddEntry( sigh[0], 'W`_{R} at 1500 GeV', 'L')
leg.AddEntry( sigh[1], 'W`_{R} at 1900 GeV', 'L')
leg.AddEntry( sigh[2], 'W`_{R} at 2300 GeV', 'L')

#c1.cd()
#c1.SetLeftMargin(0.17)
#st1.GetXaxis().SetRangeUser(0,3000)
st1.SetMaximum(DataTOTALBEH.GetMaximum() * 1.3)
st1.SetMinimum(1.0)
st1.SetTitle(';M_{tb} (GeV);Counts per 100 GeV')
st1.Draw("hist")
gPad.SetLeftMargin(.16)
st1.GetYaxis().SetTitleOffset(0.9)
#DataTOTALBEH.Draw("histsame")
#DataTOTALBEL.Draw("histsame")
sigst.Draw("samehist")
bkgline.Draw("samehist")
sigh[0].Draw("samehist")
sigh[1].Draw("samehist")
sigh[2].Draw("samehist")


DataFS1	    = TH1D("DataFS1",     "mass W' in b+1",     	  	      140, 500, 4000 )
DataFS1 = DataFS1.Rebin(len(bins2)-1,"",bins2)
for ibin in range(1,DataFS.GetNbinsX()+1):
	DataFS1.SetBinContent(ibin,DataFS.GetBinContent(ibin))

DataFS1.SetBinErrorOption(DataFS1.kPoisson)
DataFS1.Draw("samepE")

leg.Draw()
prelim = TLatex()
prelim.SetNDC()


insertlogo( main, 2, 11 )


#prelim.DrawLatex( 0.5, 0.91, "#scale[0.8]{CMS Preliminary, 8 TeV, 19.7 fb^{-1}}" )
sub.cd()
gPad.SetLeftMargin(.16)
totalH = st1.GetStack().Last().Clone("totalH")
#totalH.Add(TTmcFS)
pull = Make_Pull_plot( DataFS1,totalH,DataTOTALBEH,DataTOTALBEL )


	
#pull.GetXaxis().SetRangeUser(0,3000)
pull.SetFillColor(TROOT.kBlue)
pull.SetTitle(';M_{tb} (GeV);(Data-Bkg)/#sigma')
pull.SetStats(0)


pull.GetYaxis().SetRangeUser(-2.9,2.9)
pull.GetXaxis().SetLabelSize(0.05)
pull.GetYaxis().SetLabelSize(0.05)


LS = .13

pull.GetYaxis().SetTitleOffset(0.4)
pull.GetXaxis().SetTitleOffset(0.9)
pull.SetStats(0)
    
    
pull.GetYaxis().SetLabelSize(LS)
pull.GetYaxis().SetTitleSize(LS)
pull.GetYaxis().SetNdivisions(306)
pull.GetXaxis().SetLabelSize(LS)
pull.GetXaxis().SetTitleSize(LS)

pull.Draw("hist")

line2=ROOT.TLine(500.0,0.0,4000.0,0.0)
line2.SetLineColor(0)
line1=ROOT.TLine(500.0,0.0,4000.0,0.0)
line1.SetLineStyle(2)

line2.Draw()
line1.Draw()
gPad.Update()

main.RedrawAxis()

c1.Print('plots/MtwvsBkg_BifPoly_fit_PSET_'+options.cuts+'.root', 'root')
c1.Print('plots/MtwvsBkg_BifPoly_fit_PSET_'+options.cuts+'.pdf', 'pdf')
c1.Print('plots/MtwvsBkg_BifPoly_fit_PSET_'+options.cuts+'.png', 'png')
main.SetLogy()
st1.SetMaximum( DataBEh.GetMaximum() * 5000 )
st1.SetMinimum( 0.1)
main.RedrawAxis()

c1.Print('plots/MtwvsBkgsemilog_BifPoly_fit_PSET_'+options.cuts+'.root', 'root')
c1.Print('plots/MtwvsBkgsemilog_BifPoly_fit_PSET_'+options.cuts+'.pdf', 'pdf')
c1.Print('plots/MtwvsBkgsemilog_BifPoly_fit_PSET_'+options.cuts+'.png', 'png')

