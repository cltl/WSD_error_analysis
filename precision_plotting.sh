
#check if enough arguments are passed, else print usage information
if [ $# -eq 0 ];
then
echo
echo "Usage:                  : $0 competitions"
echo
echo "competitions            : concatenated by underscore the competitions\
you want to include. Options are sval2 sval3 sval2007 sval2010 sval2013"
echo "feature                 : pos | freq_class"
echo "top x rankings          : top x rankings taken into account"
echo "unranked                : yes | no"
echo
echo 'example of call:'
echo 'bash pos_errors.sh sval2_sval3 1 no'
echo
echo "the output path of the graph will be shown in the terminal"
exit -1;
fi

#assign command line arguments to variables and obtain basename
export cwd=/${PWD#*/}
export competitions=$1
export feature=$2
export rankings=$3
export unranked=$4
export output_path_pdf=$cwd/output/pos_errors/$competitions+++$feature+++$rankings+++$unranked.pdf
export barplot_path_pdf=$cwd/output/pos_errors/$competitions+++$feature+++$rankings+++$unranked__barplot.pdf

#call python script
python lib/precision_plotting.py

#echo path to user
echo
echo "graph can be found at:"
echo $output_path_pdf