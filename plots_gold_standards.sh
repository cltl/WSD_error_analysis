
#check if enough arguments are passed, else print usage information
if [ $# -eq 0 ];
	then
	echo
	echo "Usage:                  : $0 competitions allowed_pos"
	echo
	echo "competitions            : concatenated by underscore the competitions\
	you want to include. Options are sval2 sval3 sval2007 sval2010 sval2013"
	echo "allowed_pos             : concatenated by underscore the pos you want\
	to include. Options are: n, v, a, r, u."
	echo
	echo 'example of call:'
	echo 'bash plots_gold_standards.sh sval2_sval3 n_v_a'
	exit -1;
fi

#assign command line arguments to variables
export cwd=/${PWD#*/}
export competitions=$1
export allowed_pos=$2

#rm and create output folder
export output_folder=$cwd/output/gs_analysis/$competitions+++$allowed_pos
export output_path=$output_folder/predominant_sense.pdf

rm -rf $output_folder && mkdir $output_folder

#call python script
python lib/gold_standard_analysis.py

#echo output information to user
echo
echo 'output folder can be found here:' 
echo $output_folder
echo "this folder contains files with suffix .csv"
echo "these files contain the sentences for lemmas that are used in more than one sense in a discourse level instance"

echo "this folder also contains files with suffix stats.csv"
echo "these files show the number of occurences per lemma in which this lemma is used in a different sense than the predominant one"
echo
echo 'path to plot:'
echo $output_path
