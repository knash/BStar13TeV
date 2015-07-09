import ROOT, sys, os, re, string
from ROOT import *

xsec = {'800':2.981,'900':1.449,'1000':0.7361,'1100':0.3886,'1200':0.2113,'1300':0.1182,'1400':0.0678,'1500':0.03964,'1600':0.0236,'1700':0.01427,'1800':0.008739,'1900':0.005439,'2000':0.003422}

ListBstarMass_had = ['bs800','bs900','bs1000','bs1100','bs1200','bs1300','bs1400','bs1500','bs1600','bs1700','bs1800','bs1900','bs2000']
ListBstarMass_lepR = ['BstarRight800','BstarRight900','BstarRight1000','BstarRight1100','BstarRight1200','BstarRight1300','BstarRight1400','BstarRight1500','BstarRight1600','BstarRight1700','BstarRight1800','BstarRight1900','BstarRight2000']
ListBstarMass_lepL = ['BstarLeft800','BstarLeft900','BstarLeft1000','BstarLeft1100','BstarLeft1200','BstarLeft1300','BstarLeft1400','BstarLeft1500','BstarLeft1600','BstarLeft1700','BstarLeft1800','BstarLeft1900','BstarLeft2000']
ListBstarMass_lepV = ['BstarVector800','BstarVector900','BstarVector1000','BstarVector1100','BstarVector1200','BstarVector1300','BstarVector1400','BstarVector1500','BstarVector1600','BstarVector1700','BstarVector1800','BstarVector1900','BstarVector2000']
RootFiles = {}

RootFiles['semilep'] = TFile("template_Bstar_lepPt_130-newPDFnewQCDWJETS.root")
RootFiles['Right_had'] = TFile("allhadronicright_mtw.root")
RootFiles['Left_had'] = TFile("allhadronicleft_mtw.root")
RootFiles['Vector_had'] = TFile("allhadronicvectorlike_mtw.root")
RootFiles['Right_dilep']  = TFile("HistoForShapeLimitbStarDileptonRight.root")
RootFiles['Left_dilep']  = TFile("HistoForShapeLimitbStarDileptonLeft.root")
RootFiles['Vector_dilep']  = TFile("HistoForShapeLimitbStarDileptonVector.root")

def prepare_hists():
       
    f_lepr = TFile("BStarCombinationHistos_Right_Semileptonic.root", "RECREATE")
    f_lepr.cd()

    for key in RootFiles['semilep'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['semilep'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())
        if (name.find("TTBar")>0): name = name.replace("TTBar","ttbar")
        if (name.find("QCD")>0): name = name.replace("QCD","qcd")
        if (name.find("allSChannel")>0): name = name.replace("allSChannel","sts")
        if (name.find("allTChannel")>0): name = name.replace("allTChannel","stt")
        if (name.find("_tW")>0): name = name.replace("_tW","_sttW")
        newhist.SetName(name)
        newhist.SetTitle(name)
        isbs = name.find("Bstar")

        for Mass in ListBstarMass_lepR:
            bs = name.find(Mass)
            if (bs>0) :
        	name = name.replace("BstarRight","bs")
        	newhist.SetName(name)
        	newhist.SetTitle(name)
                newhist.Write()
 
        if (not isbs>0): newhist.Write()
    
    f_lepr.Close()

    f_lepl = TFile("BStarCombinationHistos_Left_Semileptonic.root", "RECREATE")
    f_lepl.cd()

    for key in RootFiles['semilep'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['semilep'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())
        if (name.find("TTBar")>0): name = name.replace("TTBar","ttbar")
        if (name.find("QCD")>0): name = name.replace("QCD","qcd")
        if (name.find("allSChannel")>0): name = name.replace("allSChannel","sts")
        if (name.find("allTChannel")>0): name = name.replace("allTChannel","stt")
        if (name.find("_tW")>0): name = name.replace("_tW","_sttW")
        newhist.SetName(name)
        newhist.SetTitle(name) 
        isbs = name.find("Bstar")

        for Mass in ListBstarMass_lepL:
            bs = name.find(Mass)
            if (bs>0) :
        	name = name.replace("BstarLeft","bs")
        	newhist.SetName(name)
        	newhist.SetTitle(name)
                newhist.Write()
 
        if (not isbs>0): newhist.Write()
    
    f_lepl.Close()

    f_lepv = TFile("BStarCombinationHistos_Vector_Semileptonic.root", "RECREATE")
    f_lepv.cd()

    for key in RootFiles['semilep'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['semilep'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())
        if (name.find("TTBar")>0): name = name.replace("TTBar","ttbar")
        if (name.find("QCD")>0): name = name.replace("QCD","qcd")
        if (name.find("allSChannel")>0): name = name.replace("allSChannel","sts")
        if (name.find("allTChannel")>0): name = name.replace("allTChannel","stt")
        if (name.find("_tW")>0): name = name.replace("_tW","_sttW")
        newhist.SetName(name)
        newhist.SetTitle(name)
        isbs = name.find("Bstar")

        for Mass in ListBstarMass_lepV:
            bs = name.find(Mass)
            if (bs>0) :
        	name = name.replace("BstarVector","bs")
        	newhist.SetName(name)
        	newhist.SetTitle(name)
                newhist.Write()
 
        if (not isbs>0): newhist.Write()
    
    f_lepv.Close()


    f_dilepr = TFile("BStarCombinationHistos_Right_Dileptonic.root", "RECREATE")
    f_dilepr.cd()

    for key in RootFiles['Right_dilep'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['Right_dilep'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())
	if (name.find("ttbar__scale__plus")>=0): name = name.replace("ttbar__scale__plus","mtw_dilepton__ttbar__Q2__plus")
	if (name.find("ttbar__scale__minus")>=0): name = name.replace("ttbar__scale__minus","mtw_dilepton__ttbar__Q2__minus")
	if (name.find("mtw_dilepton")<0 and name.find("data_obs")<0) : continue
	if (name.find("stats")>0) : continue   ### no need of MC statistical uncertainties templates. 
        if (name.find("TotalUncertainty")>0) : continue  
        if (name.find("data_obs")>=0): name = name.replace("data_obs","mtw_dilepton__DATA")
        if (name.find("left800")>0) : continue  

        newhist.SetName(name)
        newhist.SetTitle(name)

        #isbs = name.find("bs")

        #for Mass in ListBstarMass_had:
        #    bs = name.find(Mass)
        #    if (bs>0) :
        #        rt_xsec_had = xsec[Mass.lstrip('bs')]*0.676*0.676
        #        print 'Scaling ',name,' by ',str(rt_xsec_had)
        #        newhist.Scale(rt_xsec_had)
        #        newhist.Write()
        #        rt_xsec_had = 0.0

        #if (not isbs>0): 
	newhist.Write()
    f_dilepr.Close()


    f_dilepl = TFile("BStarCombinationHistos_Left_Dileptonic.root", "RECREATE")
    f_dilepl.cd()

    for key in RootFiles['Left_dilep'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['Left_dilep'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())
	if (name.find("ttbar__scale__plus")>=0): name = name.replace("ttbar__scale__plus","mtw_dilepton__ttbar__Q2__plus")
	if (name.find("ttbar__scale__minus")>=0): name = name.replace("ttbar__scale__minus","mtw_dilepton__ttbar__Q2__minus")
        if (name.find("mtw_dilepton")<0 and name.find("data_obs")<0) : continue
        if (name.find("stats")>0) : continue   ### no need of MC statistical uncertainties templates. 
        if (name.find("TotalUncertainty")>0) : continue  
        if (name.find("left800")>0) : continue   
        if (name.find("data_obs")>=0): name = name.replace("data_obs","mtw_dilepton__DATA")

        newhist.SetName(name)
        newhist.SetTitle(name)

        #isbs = name.find("bs")

        #if (not isbs>0): 
	newhist.Write()
    f_dilepl.Close()

    f_dilepv = TFile("BStarCombinationHistos_Vector_Dileptonic.root", "RECREATE")
    f_dilepv.cd()

    for key in RootFiles['Vector_dilep'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['Vector_dilep'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())
	if (name.find("ttbar__scale__plus")>=0): name = name.replace("ttbar__scale__plus","mtw_dilepton__ttbar__Q2__plus")
	if (name.find("ttbar__scale__minus")>=0): name = name.replace("ttbar__scale__minus","mtw_dilepton__ttbar__Q2__minus")
        if (name.find("mtw_dilepton")<0 and name.find("data_obs")<0) : continue
        if (name.find("stats")>0) : continue   ### no need of MC statistical uncertainties templates. 
        if (name.find("TotalUncertainty")>0) : continue  
        if (name.find("data_obs")>=0): name = name.replace("data_obs","mtw_dilepton__DATA")
        if (name.find("left800")>0) : continue   
        newhist.SetName(name)
        newhist.SetTitle(name)

        #isbs = name.find("bs")

        #if (not isbs>0): 
	newhist.Write()
    f_dilepv.Close()


    f_hadr = TFile("BStarCombinationHistos_Right_Allhadronic.root", "RECREATE")
    f_hadr.cd()

    for key in RootFiles['Right_had'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['Right_had'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())

        if (name.find("__up")>0): name = name.replace("__up","__plus")
        if (name.find("__down")>0): name = name.replace("__down","__minus")

        newhist.SetName(name)
        newhist.SetTitle(name)


        for Mass in ListBstarMass_had:
            newhist.Write()

    f_hadr.Close()
   
    f_hadl = TFile("BStarCombinationHistos_Left_Allhadronic.root", "RECREATE")
    f_hadl.cd()

    for key in RootFiles['Left_had'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['Left_had'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())

        if (name.find("__up")>0): name = name.replace("__up","__plus")
        if (name.find("__down")>0): name = name.replace("__down","__minus")

        newhist.SetName(name)
        newhist.SetTitle(name)

        for Mass in ListBstarMass_had:
            newhist.Write()
    f_hadl.Close()

    f_hadv = TFile("BStarCombinationHistos_Vector_Allhadronic.root", "RECREATE")
    f_hadv.cd()

    for key in RootFiles['Vector_had'].GetListOfKeys():

        print 'Name / Title = ',key.GetName(),' / ',key.GetTitle()

        hist = RootFiles['Vector_had'].Get( str(key.GetName()) )
        newhist = hist.Clone()
        name = str(key.GetName())

        if (name.find("__up")>0): name = name.replace("__up","__plus")
        if (name.find("__down")>0): name = name.replace("__down","__minus")

        newhist.SetName(name)
        newhist.SetTitle(name)

        for Mass in ListBstarMass_had:
            newhist.Write()

 
    f_hadv.Close()
prepare_hists()
                        
