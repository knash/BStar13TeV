#! /bin/sh
tar czvf analysis.tgz  analysis thetaGridbs.sh thetaGridbs.py BStarCombinationHistos_Left_Allhadronic.root BStarCombinationHistos_Left_Semileptonic.root  BStarCombinationHistos_Right_Allhadronic.root  BStarCombinationHistos_Right_Semileptonic.root  BStarCombinationHistos_Vector_Allhadronic.root  BStarCombinationHistos_Vector_Semileptonic.root  BStarCombinationHistos_Left_Dileptonic.root  BStarCombinationHistos_Right_Dileptonic.root  BStarCombinationHistos_Vector_Dileptonic.root  gridpack_bsTemplate.tgz

../../../development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=analysis.tgz \theta.listOfJobs commands.cmd
../../../runManySections.py --submitCondor commands.cmd
condor_q knash
