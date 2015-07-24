#! /bin/sh
tar czvf tarball.tgz fitdata ModMassFile.root Tagrate2D.root rootlogon.C TWkinematics.py TWsequencer.py Bstar_Functions.py TWrate.py Triggerweight_signalright2000.root PileUp_Ratio_ttbar.root PileUp_Ratio_signal*.root 
./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \kin.listOfJobs commands.cmd
./runManySections.py --submitCondor commands.cmd
condor_q knash
