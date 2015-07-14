rm resultsright/had/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_right_had/*.txt resultsright/had/
cat resultsright/had/*observed*.txt | grep -v "# x; y" >resultsright/had/observed_limits.txt
cat resultsright/had/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsright/had/expected_limits.txt
cd resultsright/had/
python limit_plot_shape.py --coupling=right --channel=had --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../


rm resultsright/semilep/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_right_semilep/*.txt resultsright/semilep/
cat resultsright/semilep/*observed*.txt | grep -v "# x; y" >resultsright/semilep/observed_limits.txt
cat resultsright/semilep/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsright/semilep/expected_limits.txt
cd resultsright/semilep/
python limit_plot_shape.py --coupling=right --channel=semilep --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsright/comb/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_right_comb/*.txt resultsright/comb/
cat resultsright/comb/*observed*.txt | grep -v "# x; y" >resultsright/comb/observed_limits.txt
cat resultsright/comb/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsright/comb/expected_limits.txt
cd resultsright/comb/
python limit_plot_shape.py --coupling=right --channel=comb --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsright/dilep/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_right_dilep/*.txt resultsright/dilep/
cat resultsright/dilep/*observed*.txt | grep -v "# x; y" >resultsright/dilep/observed_limits.txt
cat resultsright/dilep/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsright/dilep/expected_limits.txt
cd resultsright/dilep/
python limit_plot_shape.py --coupling=right --channel=dilep --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsleft/had/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_left_had/*.txt resultsleft/had/
cat resultsleft/had/*observed*.txt | grep -v "# x; y" >resultsleft/had/observed_limits.txt
cat resultsleft/had/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsleft/had/expected_limits.txt
cd resultsleft/had/
python limit_plot_shape.py --coupling=left --channel=had --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsleft/semilep/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_left_semilep/*.txt resultsleft/semilep/
cat resultsleft/semilep/*observed*.txt | grep -v "# x; y" >resultsleft/semilep/observed_limits.txt
cat resultsleft/semilep/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsleft/semilep/expected_limits.txt
cd resultsleft/semilep/
python limit_plot_shape.py --coupling=left --channel=semilep --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsleft/comb/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_left_comb/*.txt resultsleft/comb/
cat resultsleft/comb/*observed*.txt | grep -v "# x; y" >resultsleft/comb/observed_limits.txt
cat resultsleft/comb/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsleft/comb/expected_limits.txt
cd resultsleft/comb/
python limit_plot_shape.py --coupling=left --channel=comb --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsleft/dilep/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_left_dilep/*.txt resultsleft/dilep/
cat resultsleft/dilep/*observed*.txt | grep -v "# x; y" >resultsleft/dilep/observed_limits.txt
cat resultsleft/dilep/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsleft/dilep/expected_limits.txt
cd resultsleft/dilep/
python limit_plot_shape.py --coupling=left --channel=dilep --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsvector/had/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_vector_had/*.txt resultsvector/had/
cat resultsvector/had/*observed*.txt | grep -v "# x; y" >resultsvector/had/observed_limits.txt
cat resultsvector/had/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsvector/had/expected_limits.txt
cd resultsvector/had/
python limit_plot_shape.py --coupling=vector --channel=had --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsvector/semilep/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_vector_semilep/*.txt resultsvector/semilep/
cat resultsvector/semilep/*observed*.txt | grep -v "# x; y" >resultsvector/semilep/observed_limits.txt
cat resultsvector/semilep/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsvector/semilep/expected_limits.txt
cd resultsvector/semilep/
python limit_plot_shape.py --coupling=vector --channel=semilep --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsvector/comb/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_vector_comb/*.txt resultsvector/comb/
cat resultsvector/comb/*observed*.txt | grep -v "# x; y" >resultsvector/comb/observed_limits.txt
cat resultsvector/comb/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsvector/comb/expected_limits.txt
cd resultsvector/comb/
python limit_plot_shape.py --coupling=vector --channel=comb --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

rm resultsvector/dilep/*limits*.txt
cp ../limitsetting/theta/analysis_bstar_vector_dilep/*.txt resultsvector/dilep/
cat resultsvector/dilep/*observed*.txt | grep -v "# x; y" >resultsvector/dilep/observed_limits.txt
cat resultsvector/dilep/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsvector/dilep/expected_limits.txt
cd resultsvector/dilep/
python limit_plot_shape.py --coupling=vector --channel=dilep --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../
