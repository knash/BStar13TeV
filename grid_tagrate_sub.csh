#! /bin/sh
tar czvf tarball.tgz Wprime_Functions.py TBrate.py TRIG_EFFICWPHTdata_dijet8TeV.root PileUp_Ratio_ttbar.root PileUp_Ratio_signal*.root 
/uscms_data/d3/knash/development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \tagrate.listOfJobs commands.cmd
/uscms_data/d3/knash/runManySections.py --submitCondor commands.cmd
condor_q knash
