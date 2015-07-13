cp BStarCombination/BStarCombinationHistos*.root ./

sed 's/RTYPE/comb/g' analysis_bsTEMPLATE.py > analysis_bsright_Combination.py 
sed -i 's/RSTEP/0/g' analysis_bsright_Combination.py 
sed -i 's/RSIG/Right/g' analysis_bsright_Combination.py

sed 's/RTYPE/had/g' analysis_bsTEMPLATE.py >  analysis_bsright_AllHad.py
sed -i 's/RSTEP/0/g' analysis_bsright_AllHad.py
sed -i 's/RSIG/Right/g' analysis_bsright_AllHad.py


sed 's/RTYPE/semilep/g' analysis_bsTEMPLATE.py >  analysis_bsright_Semilep.py
sed -i 's/RSTEP/0/g' analysis_bsright_Semilep.py
sed -i 's/RSIG/Right/g' analysis_bsright_Semilep.py


sed 's/RTYPE/dilep/g' analysis_bsTEMPLATE.py > analysis_bsright_dilep.py 
sed -i 's/RSTEP/0/g' analysis_bsright_dilep.py 
sed -i 's/RSIG/Right/g' analysis_bsright_dilep.py 


sed 's/RTYPE/comb/g' analysis_bsTEMPLATE.py > analysis_bsleft_Combination.py 
sed -i 's/RSTEP/0/g' analysis_bsleft_Combination.py 
sed -i 's/RSIG/Left/g' analysis_bsleft_Combination.py


sed 's/RTYPE/had/g' analysis_bsTEMPLATE.py >  analysis_bsleft_AllHad.py
sed -i 's/RSTEP/0/g' analysis_bsleft_AllHad.py
sed -i 's/RSIG/Left/g' analysis_bsleft_AllHad.py


sed 's/RTYPE/semilep/g' analysis_bsTEMPLATE.py >  analysis_bsleft_Semilep.py
sed -i 's/RSTEP/0/g' analysis_bsleft_Semilep.py
sed -i 's/RSIG/Left/g' analysis_bsleft_Semilep.py


sed 's/RTYPE/dilep/g' analysis_bsTEMPLATE.py > analysis_bsleft_dilep.py 
sed -i 's/RSTEP/0/g' analysis_bsleft_dilep.py 
sed -i 's/RSIG/Left/g' analysis_bsleft_dilep.py 





sed 's/RTYPE/comb/g' analysis_bsTEMPLATE.py > analysis_bsvector_Combination.py 
sed -i 's/RSTEP/0/g' analysis_bsvector_Combination.py 
sed -i 's/RSIG/Vector/g' analysis_bsvector_Combination.py


sed 's/RTYPE/had/g' analysis_bsTEMPLATE.py >  analysis_bsvector_AllHad.py
sed -i 's/RSTEP/0/g' analysis_bsvector_AllHad.py
sed -i 's/RSIG/Vector/g' analysis_bsvector_AllHad.py


sed 's/RTYPE/semilep/g' analysis_bsTEMPLATE.py >  analysis_bsvector_Semilep.py
sed -i 's/RSTEP/0/g' analysis_bsvector_Semilep.py
sed -i 's/RSIG/Vector/g' analysis_bsvector_Semilep.py


sed 's/RTYPE/dilep/g' analysis_bsTEMPLATE.py > analysis_bsvector_dilep.py 
sed -i 's/RSTEP/0/g' analysis_bsvector_dilep.py 
sed -i 's/RSIG/Vector/g' analysis_bsvector_dilep.py 



python grid_submit_theta.py --file=analysis_bsright_Combination.py --uidir=analysis_bstar_right_comb
python grid_submit_theta.py --file=analysis_bsright_AllHad.py --uidir=analysis_bstar_right_had
python grid_submit_theta.py --file=analysis_bsright_Semilep.py --uidir=analysis_bstar_right_semilep
python grid_submit_theta.py --file=analysis_bsright_dilep.py --uidir=analysis_bstar_right_dilep

python grid_submit_theta.py --file=analysis_bsleft_Combination.py --uidir=analysis_bstar_left_comb
python grid_submit_theta.py --file=analysis_bsleft_AllHad.py --uidir=analysis_bstar_left_had
python grid_submit_theta.py --file=analysis_bsleft_Semilep.py --uidir=analysis_bstar_left_semilep
python grid_submit_theta.py --file=analysis_bsleft_dilep.py --uidir=analysis_bstar_left_dilep

python grid_submit_theta.py --file=analysis_bsvector_Combination.py --uidir=analysis_bstar_vector_comb
python grid_submit_theta.py --file=analysis_bsvector_AllHad.py --uidir=analysis_bstar_vector_had
python grid_submit_theta.py --file=analysis_bsvector_Semilep.py --uidir=analysis_bstar_vector_semilep
python grid_submit_theta.py --file=analysis_bsvector_dilep.py --uidir=analysis_bstar_vector_dilep


