
#check if enough arguments are passed, else print usage information
if [ $# -eq 0 ];
	then
	echo
	echo "Usage:                  : $0 competition"
	echo
	echo "competition            : concatenated by underscore the competitions\
	you want to include. Options are sval2 sval3 sval2007 sval2010 sval2013"
	echo 
	echo 'example of call:'
	echo 'bash provide_stats_gs.sh sval2'
	echo
	echo 'output will be written to output/stats_gs/'
	echo
	exit -1;
fi

#assign command line arguments to variables
export cwd=/${PWD#*/}
export competition=$1

#create output folder if needed
export output_folder=$cwd/output/gs_stats
mkdir -p $output_folder
export output_path=$output_folder/$competition.txt

#call python script
python lib/stats_gs.py

#echo output information to user
echo
echo 'output can be found at:'
echo $output_path
