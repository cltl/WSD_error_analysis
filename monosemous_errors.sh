
#check if enough arguments are passed, else print usage information
if [ $# -eq 0 ];
then
    echo
    echo "Usage:                  : $0 competitions allowed_pos"
    echo
    echo "competitions            : concatenated by underscore the competitions\
    you want to include. Options are sval2 sval3 sval2007 sval2010 sval2013"
    echo "top x rankings          : top x rankings taken into account"
    echo "unranked                : yes | no"
    echo
    echo 'example of call:'
    echo 'bash monosemous_errors.sh sval2_sval3 1 no'
    echo
    echo "the output path of the graph will be shown in the terminal"
    exit -1;
fi

#assign command line arguments to variables and obtain basename
export cwd=/${PWD#*/}
export competitions=$1
export rankings=$2
export unranked=$3
export output_path_txt=$cwd/output/monosemous_errors/$competitions+++$allowed_pos+++$rankings+++$unranked.txt

#call python script
python lib/monosemous_errors.py

#echo output information for user
echo $output_path_txt
