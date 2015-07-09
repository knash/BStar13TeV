import array, math

def Inter(g1,g2):
	xaxisrange = g1.GetXaxis().GetXmax()-g1.GetXaxis().GetXmin()
	xaxismin = g1.GetXaxis().GetXmin()
	inters = []
	for x in range(0,10000):
		xpoint = xaxismin + (float(x)/1000.0)*xaxisrange
		xpoint1 = xaxismin + (float(x+1)/1000.0)*xaxisrange
		Pr1 = g1.Eval(xpoint)
		Pr2 = g2.Eval(xpoint)
		Po1 = g1.Eval(xpoint1)
		Po2 = g2.Eval(xpoint1)
		if (Pr1-Pr2)*(Po1-Po2)<0:
			inters.append(0.5*(xpoint+xpoint1))
		
	return inters
			
def strf( x ):
	return '%.3f' % x

def strf1( x ):
	return '%.0f' % x
	

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFileExp', metavar='H', type='string', action='store',
                  default='limits_shape_exp.txt',
                  dest='inputFileExp',
                  help='Expected limits from theta')

parser.add_option('--inputFileObs', metavar='H', type='string', action='store',
                  default='limits_shape_obs.txt',
                  dest='inputFileObs',
                  help='Observed limits from theta')

parser.add_option('--outputName', metavar='D', type='string', action='store',
                  default='comb',
                  dest='outputName',
                  help='Directory to plot')
parser.add_option('--channel', metavar='D', type='string', action='store',
                  default='had',
                  dest='channel',
                  help='had,semilep,comb')
parser.add_option('--coupling', metavar='D', type='string', action='store',
                  default='right',
                  dest='coupling',
                  help='right,left,vector')

parser.add_option('--title', metavar='D', type='string', action='store',
                  default='narrow',
                  dest='title',
                  help='Titles to use, options are narrow, wide, kkg')

parser.add_option('--showNarrowTheory', action='store_true',
                  default=False,
                  dest='showNarrowTheory',
                  help='Show theory prediction for 1% width')

parser.add_option('--showWideTheory', action='store_true',
                  default=False,
                  dest='showWideTheory',
                  help='Show theory prediction for 3% width')

parser.add_option('--showKKGTheory', action='store_true',
                  default=False,
                  dest='showKKGTheory',
                  help='Show theory prediction for KK Gluon')

parser.add_option('--useLog', metavar='L', action='store_true',
                  default=False,
                  dest='useLog',
                  help='use log y-axis')

parser.add_option('--noTheory', metavar='T', action='store_true',
                  default=False,
                  dest='noTheory',
                  help='do not plot theory curves')

(options, args) = parser.parse_args()

argv = []

from ROOT import *
import ROOT
    
def make_smooth_graph(h2,h3):
    h2 = TGraph(h2)
    h3 = TGraph(h3)
    npoints = h3.GetN()
    h3.Set(2*npoints+2)
    for b in range(npoints+2):
        x1, y1 = (ROOT.Double(), ROOT.Double())
        if b == 0:
            h3.GetPoint(npoints-1, x1, y1)
        elif b == 1:
            h2.GetPoint(npoints-b, x1, y1)
        else:
            h2.GetPoint(npoints-b+1, x1, y1)
        h3.SetPoint(npoints+b, x1, y1)
    return h3

if __name__ == "__main__":
    ROOT.gROOT.Macro("rootlogon.C")
    TPT = ROOT.TPaveText(.20, .22, .5, .27,"NDC")
    if options.channel=="had":
    	TPT.AddText("All-Hadronic Channel")
    if options.channel=="semilep":
    	TPT.AddText("Semileptonic Channel")
    if options.channel=="dilep":
    	TPT.AddText("Dileptonic Channel")
    if options.channel=="comb":
    	TPT.AddText("Combined")
    TPT.SetFillColor(0)
    TPT.SetBorderSize(0)
    TPT.SetTextAlign(12)
    xsec = {'800':2.981,'900':1.449,'1000':0.7361,'1100':0.3886,'1200':0.2113,'1300':0.1182,'1400':0.0678,'1500':0.03964,'1600':0.0236,'1700':0.01427,'1800':0.008739,'1900':0.005439,'2000':0.003422}
    xsecup = {'800':3.396,'900':1.661,'1000':0.8488,'1100':0.4507,'1200':0.2462,'1300':0.1384,'1400':0.07952,'1500':0.04662,'1600':0.02785,'1700':0.01687,'1800':0.01038,'1900':0.006462,'2000':0.004071}
    xsecdown = {'800':2.626,'900':1.267,'1000':0.6413,'1100':0.3365,'1200':0.1828,'1300':0.1019,'1400':0.05813,'1500':0.03386,'1600':0.02014,'1700':0.01214,'1800':0.00744,'1900':0.004607,'2000':0.002896}
    mult=0.0
    if options.coupling == "right":
	mult = 1.0
	cstr = "R"
    if options.coupling == "left":
	mult = 1.0
	cstr = "L"
    if options.coupling == "vector":
	mult = 2.0
	cstr = "LR"

    masses = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600,1700,1800,1900,2000] 
    x_mass = array.array('d')

    y_limit = array.array('d')
    y_mclimit  = array.array('d')
    y_mclimitlow68 = array.array('d')
    y_mclimitup68 = array.array('d')
    y_mclimitup95 = array.array('d')
    y_mclimitlow95 = array.array('d')
    
    #logScale = False
    logScale = options.useLog
    #channel = "12"
    #channel = "11"
    #channel = "comb-plc"
    channel = "comb-mcmc"

    # masses = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
    # masses = [750, 1000, 1250, 1500, 2000, 3000]
    #masses = [750, 800, 900, 1000, 1100, 1200, 1250, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]
   # masses = [1000, 1100, 1300, 1400, 1500, 1700, 1800, 1900, 2000, 3000]
    
    # Initialise arrays
#    for i in range(0, len(masses)):
#        x_mass.append(0.)
#        y_limit.append(0.)
#        y_mclimit.append(0.)
#        y_mclimitlow68.append(0.)
#        y_mclimitup68.append(0.)
#        y_mclimitlow95.append(0.)
#        y_mclimitup95.append(0.)

    #--- Open this file with points. We expect six columns.
    f1 = file(options.inputFileExp, "r")
    f2 = file(options.inputFileObs, "r")

    # i = 0
    for line in f1:

        data = map(float,line.split())
        rt_xsec = mult*xsec[str(int(data[0]))]
        #print data
        # data is an array along the line, has 8 entries
        x_mass.append( data[0]/1000.0  )    # mass
        #y_limit.append( data[1] )
        y_mclimit.append( data[1]*rt_xsec )
        y_mclimitlow95.append( data[2]*rt_xsec )
        y_mclimitup95.append( data[3]*rt_xsec )
        y_mclimitlow68.append( data[4]*rt_xsec )
        y_mclimitup68.append( data[5]*rt_xsec )

    # i = 0
    for line in f2:
        data = map(float,line.split())
        rt_xsec = mult*xsec[str(int(data[0]))]
        #print data
        y_limit.append( data[1]*rt_xsec )
    #print "Limit Table"
    #for imass in range(0,len(x_mass)):    
    	#if x_mass[imass] == 1.3 or x_mass[imass] == 1.5 or x_mass[imass] == 1.7 or x_mass[imass] == 1.9 or x_mass[imass] == 2.1 or x_mass[imass] == 2.3 or x_mass[imass] == 2.7 or x_mass[imass] == 3.1:
		#print "\hline"
		#print strf1(x_mass[imass]*1000.0) +" & "+strf(y_limit[imass])+" & "+strf(y_mclimit[imass])+" & "+strf(y_mclimitlow68[imass])+","+strf(y_mclimitup68[imass])+" & "+strf(y_mclimitlow95[imass])+","+strf(y_mclimitup95[imass])
    print "Limit Table"
    for imass in range(0,len(x_mass)):    
    	#if x_mass[imass] == 1.3 or x_mass[imass] == 1.5 or x_mass[imass] == 1.7 or x_mass[imass] == 1.9 or x_mass[imass] == 2.1 or x_mass[imass] == 2.3 or x_mass[imass] == 2.7 or x_mass[imass] == 3.1:
		print "\hline"
		print strf1(x_mass[imass]*1000.0) +" & "+strf(y_limit[imass])+" & "+strf(y_mclimit[imass])+" & "+strf(y_mclimitlow68[imass])+","+strf(y_mclimitup68[imass])+" & "+strf(y_mclimitlow95[imass])+","+strf(y_mclimitup95[imass])
          
    cv = TCanvas("cv", "cv",700, 600)
    #cv = TCanvas("cv", "cv")
    if logScale:
        cv.SetLogy(True)
    cv.SetLeftMargin(.18)
    cv.SetBottomMargin(.18)    
    g_limit = TGraph(len(x_mass), x_mass, y_limit)
    g_limit.SetTitle("")
    g_limit.SetMarkerStyle(0)
    g_limit.SetMarkerColor(1)
    g_limit.SetLineColor(1)
    g_limit.SetLineWidth(3)
    g_limit.SetMarkerSize(0.5) #0.5
    g_limit.GetXaxis().SetTitle("M_{B*_{"+cstr+"}} (TeV)")
    g_limit.GetYaxis().SetTitle("Upper Limit #sigma_{B*_{"+cstr+"}} #times B(B*_{"+cstr+"}#rightarrowtW) [pb]")

    g_limit.Draw("alp")
    g_limit.GetYaxis().SetRangeUser(0., 80.)
    g_limit.GetXaxis().SetRangeUser(0.8, 2.0)
    if logScale:
        g_limit.SetMinimum(3.0e-3) #0.005
        g_limit.SetMaximum(7000.) #10000
    else:
        # g_limit.SetMaximum(80.)
        g_limit.SetMaximum(0.5)#20.)

    g_limit.Draw("al")
    
    g_mclimit = TGraph(len(x_mass), x_mass, y_mclimit)
    g_mclimit.SetTitle("")
    g_mclimit.SetMarkerStyle(21)
    g_mclimit.SetMarkerColor(1)
    g_mclimit.SetLineColor(1)
    g_mclimit.SetLineStyle(2)
    g_mclimit.SetLineWidth(3)
    g_mclimit.SetMarkerSize(0.)
    g_mclimit.GetXaxis().SetTitle("m_{Z'} (TeV/c^{2})")
    g_mclimit.GetYaxis().SetTitle("Upper Limit #sigma_{B*_{"+cstr+"}} #times B (pb)")
    g_mclimit.GetYaxis().SetTitleSize(0.03)
    g_mclimit.Draw("l")
    g_mclimit.GetYaxis().SetRangeUser(0., 80.)
    
    g_mcplus = TGraph(len(x_mass), x_mass, y_mclimitup68)
    g_mcminus = TGraph(len(x_mass), x_mass, y_mclimitlow68)
    
    g_mc2plus = TGraph(len(x_mass), x_mass, y_mclimitup95)
    g_mc2minus = TGraph(len(x_mass), x_mass, y_mclimitlow95)

    x_mass2 = array.array('d', [750, 1000, 1250, 1500, 2000, 3000] )
    #x_mass_fixed = array.array('d', [1, 2,3] )


#    x_mass_fixed = array.array('d', [1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8, 3.1, 3.5]) 
#    y_kkg        = array.array('d', [4.451, 1.203, 0.395, 0.150, 0.065, 0.032, 0.018, 0.011, 0.006]) 


    
    x_mass_fixed = array.array('d', [ 1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8, 3.1, 3.5
                                      ] )

    graphWP = ROOT.TGraph()
    graphWP.SetTitle("")
    graphWP.SetMarkerStyle(23)
    graphWP.SetMarkerColor(4)
    graphWP.SetLineColor(4)
    graphWP.SetLineWidth(2)
    graphWP.SetMarkerSize(0.5)
    q = 0
    for bsmass in masses:
        rt_xsec = mult*xsec[str(int(bsmass))]
    	graphWP.SetPoint(q,    bsmass/1000. ,   rt_xsec    )
	q+=1
    graphWP.SetLineWidth(3)
    graphWP.SetLineColor(4 )

    graphWPup = ROOT.TGraph()
    graphWPup.SetTitle("")
    graphWPup.SetMarkerStyle(23)
    graphWPup.SetMarkerColor(4)
    graphWPup.SetLineColor(4)
    graphWPup.SetLineWidth(2)
    graphWPup.SetMarkerSize(0.5)

    q = 0
    for bsmass in masses:
        rt_xsec = mult*xsecup[str(int(bsmass))]
    	graphWPup.SetPoint(q,    bsmass/1000. ,   rt_xsec    )
	q+=1

    graphWPdown = ROOT.TGraph()
    graphWPdown.SetTitle("")
    graphWPdown.SetMarkerStyle(23)
    graphWPdown.SetMarkerColor(4)
    graphWPdown.SetLineColor(4)
    graphWPdown.SetLineWidth(2)
    graphWPdown.SetMarkerSize(0.5)

    q = 0
    for bsmass in masses:
        rt_xsec = mult*xsecdown[str(int(bsmass))]
    	graphWPdown.SetPoint(q,    bsmass/1000. ,   rt_xsec    )
	q+=1

    graphWPup.SetLineStyle(2 )
    graphWPdown.SetLineStyle(2 )

    WPunc = make_smooth_graph(graphWPdown, graphWPup)
    WPunc.SetFillColor(4)
    WPunc.SetFillStyle(3004)
    WPunc.SetLineColor(0)

    g_error95 = make_smooth_graph(g_mc2minus, g_mc2plus)
    g_error95.SetFillColor(TROOT.kYellow)
    g_error95.SetLineColor(0)
    g_error95.Draw("lf")
    g_error95.Draw("lf")
    
    g_error = make_smooth_graph(g_mcminus, g_mcplus)
    g_error.SetFillColor( TROOT.kGreen)
    g_error.SetLineColor(0)
    g_error.Draw("lf")
    g_error.Draw("lf")
    
    WPunc.Draw("lf")

  #  g2_kkg = g_kkg.Clone()
  #  h_kkg = g_kkg.GetHistogram()
  #  g_kkg.SetLineColor(4)
  #  g_kkg.SetLineWidth(4)
  #  g_kkg.SetMarkerStyle(20)

    g_limit.Draw("l")
    g_mclimit.Draw("l")
    g_limit.Draw("l")
    graphWP.Draw("l")
    graphWPup.Draw("l")
    graphWPdown.Draw("l")
    #h_kkg.Draw("LP")

    #g_error95.SetName("g_error95");
    #g_error.SetName("g_error")
    #g_limit.SetName("g_limit")
    #g_mclimit.SetName("g_mclimit")
    #g_kkg.SetName("g_kkg")

    #Out = ROOT.TFile("output.root","RECREATE")
    #Out.cd()
    #g_error95.Write()
    #g_error.Write()
    #g_limit.Write()
    #g_mclimit.Write()
    #g_kkg.Write()
    #Out.ls()
    #Out.Write()

	#TFile *Out;
	#Out = new TFile("top_mistag_rate_NTuple.root","RECREATE");
	#Out->cd();
	#MISTAG_RATE_2011_JetPD->Write(); 
	#Out->ls();      
	#Out->Write();

    #h_limit = g_limit.GetHistogram()
    #h_error95 = g_error95.GetHistogram()
    #h_error = g_error.GetHistogram()
    #h_mclimit = g_mclimit.GetHistogram()
    #h_kkg = g_kkg.GetHistogram()

    #h_limit.SetMarkerStyle(20)
    #h_limit.SetMarkerColor(2)
    #h_limit.SetLineColor(2)
    #h_limit.SetLineWidth(2)
    #h_limit.SetMarkerSize(0.5)


    #h_limit.Draw("p")
    #h_error95.Draw("lfsame")
    #h_error.Draw("lfsame")
    #h_limit.Draw("psame")
    #h_mclimit.Draw("lsame")
    #h_kkg.Draw("lpsame")

#topJetCandEta               = ROOT.TH1F("topJetCandEta",               "topJetCandEta",            100, -4,    4)
#h_kkg->
    #legend = TLegend(0.4, 0.4, 0.9, 0.8, "")

    legLabel = ""
    if logScale:
	  legend = TLegend(0.42, 0.45, 0.86, 0.84, legLabel)
    else:
	  legend = TLegend(0.42, 0.35, 0.86, 0.75, legLabel)
    
    #legend.SetTextFont(42)
    legend.AddEntry(g_limit, "Observed (95% CL)","l")
    legend.AddEntry(g_mclimit, "Expected (95% CL)","l")
    legend.AddEntry(g_error, "#pm 1 #sigma Expected", "f")
    legend.AddEntry(g_error95, "#pm 2 #sigma Expected", "f")
    legend.AddEntry(graphWP, "Theory B*_{"+cstr+"}", "l")
  #  legend.AddEntry(graphWPup, "Theory B*_{"+cstr+"} 1 #sigma uncertainty", "l")
    g_limit.GetYaxis().SetTitleOffset(1.4)
    if not options.noTheory :
        if options.showKKGTheory :
            legend.AddEntry(g_kkg, "KK Gluon, Agashe et al", "l")
        if options.showWideTheory :
            legend.AddEntry(graphWP, "Z', 10.0% width, Harris et al", 'l')
        if options.showNarrowTheory :
            legend.AddEntry(graphZP12, "Z', 1.2% width, Harris et al", 'l')
            legend.AddEntry(graphZP30, "Z', 3.0% width, Harris et al", 'l')
#        legend.AddEntry(graphTTLambda, "New physics top scale", 'l')
#    legend.AddEntry(graphAxigluon, "Axigluon 1.1 TeV (BHKR)", 'p')


    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    
    text1 = ROOT.TLatex()
    text1.SetNDC()
    #text1.SetTextAlign(13)
    #text1.SetX(0.4) #0.32
    #text1.SetY(0.91) #0.918
    #text1.SetW(0.5)
    text1.SetTextFont(42)
    #text1.SetTextSizePixels(24)
    #text1.SetTextSizePixels(17)
    text1.DrawLatex(0.2,0.84, "#scale[1.0]{CMS, L = 19.7 fb^{-1} at  #sqrt{s} = 8 TeV}")
    
    text11 = ROOT.TLatex()
    text11.SetTextFont(42)
    text11.SetNDC()
   # if options.title == 'narrow' :
        #text11.DrawLatex(0.58, 0.84, "#scale[0.9]{W'#rightarrowtb [W#rightarrowHadrons]}")
    if options.title == 'wide' :
        text11.DrawLatex(0.58, 0.86, "#scale[1.0]{10% Width Assumption}")
    elif options.title == 'KK':
        text11.DrawLatex(0.58, 0.86, "#scale[1.0]{KK Gluon Assumption}")
    #text11.SetTextAlign(13)
    #text11.SetX(0.4) #0.32
    #text11.SetY(0.855) #0.918
    #text1.SetW(0.5)
    #text11.SetTextFont(42)
    #text1.SetTextSizePixels(24)
    #text11.SetTextSizePixels(17)
#    text11.Draw()
	
	
	
	
	#channel = "comb-plc"
	#channel = "comb-mcmc"
    label = "temp"
    
    if channel == "comb-plc":
      label = "Profile Likelihood"
    
    if channel == "comb-mcmc":
      label = "Bayesian with MCMC"
   


#    textbox = ROOT.TPaveText(0.3,0.7,0.9,0.9,"NDC");
#	textbox.SetFillColor(0);
#    textbox.SetLineColor(0);
#    line1 = ROOT.TText *line1 = textbox->AddText("CMS Preliminary");
#	line1->SetTextColor(1);
#	line1->SetTextAlign(12); //first number = horizontal alignment (1 left, 2 center, 3 right). second number =vertical alignment (1 top, 2 center, 3 bottom)
#	TText *line2 = textbox->AddText("35.97 pb^{-1} at #sqrt{s} = 7 TeV");
#	line2->SetTextColor(1);
#	line2->SetTextAlign(12); //first number = horizontal alignment (1 left, 2 center, 3 right). second number =vertical alignment (1 top, 2 center, 3 bottom)
#	textbox->Draw("same");

	#channel = "Profile Likelihood"
    #channel = "Bayesian with MCMC"
    text2 = ROOT.TLatex(3.570061, 23.08044, label)
    text2.SetNDC()
    text2.SetTextAlign(13)
    text2.SetX(0.4) #0.32
    text2.SetY(0.8) #0.87
    #text2.SetW(0.5)
    text2.SetTextFont(42)
    #text2.SetTextSizePixels(24)
    #text2.SetTextSizePixels(17)
    #text2.Draw()

	
    legend.Draw("same")
    g_limit.Draw("p same")

    postpend = options.channel + "_" + options.coupling
    if logScale:
        postpend = postpend + "_log"
    if options.noTheory :
        postpend = postpend + "_notheory"
    TPT.Draw()		
    cv.RedrawAxis()
    cv.SaveAs("limits_theta_"+postpend+".pdf")
    cv.SaveAs("limits_theta_"+postpend+".gif")
    cv.SaveAs("limits_theta_"+postpend+".png")
    cv.SaveAs("limits_theta_"+postpend+".root")

    obs = Inter(g_limit,graphWP)
    exp = Inter(g_mclimit,graphWP)
    obsup = Inter(g_limit,graphWPup)
    obsdown = Inter(g_limit,graphWPdown)
    expup = Inter(g_mclimit,graphWPup)
    expdown = Inter(g_mclimit,graphWPdown)


    print "intersections:"
    print "Observed"
    for i in range(0,len(obs)): 
    	print str(obs[i]) + " +" + str(abs(obsup[i]-obs[i])) + " -" + str(abs(obsdown[i]-obs[i]))
    print "Experimental"
    for i in range(0,len(exp)): 
    	print str(exp[i]) + " +" + str(abs(expup[i]-exp[i])) + " -" + str(abs(expdown[i]-exp[i]))

   
