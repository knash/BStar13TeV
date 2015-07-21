#! /bin/sh
tar czvf tarball.tgz fitdata ModMassFile.root Tagrate2D.root rootlogon.C TWanalyzer.py TWsequencer.py Triggerweight_signalright2000.root Bstar_Functions.py TWrate.py TRIG_EFFICWPHTdata_dijet8TeV.root PileUp_Ratio_ttbar.root PileUp_Ratio_signal*.root 

./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \ana.listOfJobs commands.cmd
./runManySections.py --submitCondor commands.cmd
condor_q knash
