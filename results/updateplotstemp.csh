rm resultsright/had/*limits*.txt
cp /uscms_data/d3/knash/BStar/NewCode/CMSSW_7_1_0/src/BStar/limitsetting/theta/analysis_bstar_right_had/*.txt resultsright/had/
cat resultsright/had/*observed*.txt | grep -v "# x; y" >resultsright/had/observed_limits.txt
cat resultsright/had/*expected*.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >resultsright/had/expected_limits.txt
cd resultsright/had/
python limit_plot_shape.py --coupling=right --channel=had --inputFileExp=expected_limits.txt --inputFileObs=observed_limits.txt --useLog --outputName=comb
cd ../../

