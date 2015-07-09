set ifile=$1
sed -i '1,11d;35,37d;61,63d;84,86d ' $ifile

sed -i 's/bs/$M_{\\bs=/g' $ifile
sed -i 's/00<\/t/00}$<\/t/g' $ifile
sed -i 's/<tr><th>//g' $ifile
sed -i 's/<tr><td>//g' $ifile
sed -i 's/<\/td><\/tr>//g' $ifile
sed -i 's/<\/td><td>/ /g' $ifile
sed -i 's/<\/sup><sub>/,/g' $ifile
sed -i 's/<sup>//g' $ifile
sed -i 's/<\/sub>//g' $ifile
sed -i 's/(s) //g' $ifile
sed -i 's/<sub>//g' $ifile
sed -i 's/<\/sup>//g' $ifile
sed -i 's/<\/td><td>//g' $ifile
sed -i 's/(r) //g' $ifile
sed -i 's/  / /g' $ifile
sed -i 's/ / \& /g' $ifile


less $ifile | cut -d '&' -f 1,2,5-8,10-12,16-18,29,30  > limittableslep.tex
less $ifile | cut -d '&' -f 1,13,21,23,25,27 > limittablehad.tex
less $ifile | cut -d '&' -f 1,15,28 > limittabledilep.tex
less $ifile | cut -d '&' -f 1,3,4,9,14,19,20,22,24,26,31 > limittablecomb.tex
