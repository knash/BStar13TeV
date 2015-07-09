sed -i 's/(model, 0)/(model, 1)/g' analysis_bsright_Combination.py 
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsright_AllHad.py
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsright_Semilep.py
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsright_dilep.py 

sed -i 's/(model, 0)/(model, 1)/g' analysis_bsleft_Combination.py 
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsleft_AllHad.py
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsleft_Semilep.py
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsleft_dilep.py 

sed -i 's/(model, 0)/(model, 1)/g' analysis_bsvector_Combination.py 
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsvector_AllHad.py
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsvector_Semilep.py
sed -i 's/(model, 0)/(model, 1)/g' analysis_bsvector_dilep.py 


cd analysis_bstar_right_comb/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsright_Combination.py
cd ../

cd analysis_bstar_left_comb/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsleft_Combination.py
cd ../

cd analysis_bstar_vector_comb/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsvector_Combination.py
cd ../


cd analysis_bstar_right_had/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsright_AllHad.py
cd ../

cd analysis_bstar_left_had/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsleft_AllHad.py
cd ../

cd analysis_bstar_vector_had/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsvector_AllHad.py
cd ../


cd analysis_bstar_right_semilep/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsright_Semilep.py
cd ../

cd analysis_bstar_left_semilep/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsleft_Semilep.py
cd ../

cd analysis_bstar_vector_semilep/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsvector_Semilep.py
cd ../


cd analysis_bstar_right_dilep/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsright_dilep.py
cd ../

cd analysis_bstar_left_dilep/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsleft_dilep.py
cd ../

cd analysis_bstar_vector_dilep/ 
cp ../run_postprocess_theta.py ./
python run_postprocess_theta.py --file=analysis_bsvector_dilep.py
cd ../



