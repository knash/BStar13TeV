set ifile=$1
sed -i '1,11d' $ifile
sed -i 's/bs/$M_{\\bs}=/g' $ifile
sed -i 's/00<\/t/00$<\/t/g' $ifile
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
less $ifile | cut -d '&' -f 1-6,8,10,12,13 
