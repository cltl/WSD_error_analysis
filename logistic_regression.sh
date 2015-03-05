
#check if enough arguments are passed, else print usage information
if [ $# -eq 0 ];
then
    echo
    echo "Usage:                  : $0 competitions allowed_pos features"
    echo
    echo "competitions            : concatenated by underscore the competitions\
    you want to include. Options are sval2 sval3 sval2007 sval2010 sval2013"
    echo "allowed_pos             : concatenated by underscore the pos you want\
    to include. Options are: n, v, a, r, u."
    echo "features                : concatenated by '---' the features you want\
    to include in the analysis. Options are: num_senses \
    len_sentence pos  copula rel_freq avg_num_senses_in_sentence MFS"
    echo "top x rankings          : top x rankings taken into account"
    echo "unranked                : yes | no"
    echo
    echo 'example of call:'
    echo 'bash logistic_regression.sh sval2_sval3 n_v_a num_senses---pos 3 no'
    echo
    echo "the output of the logistic regression will be shown in the terminal"
    exit -1;
fi

#assign command line arguments to variables and obtain basename
export cwd=/${PWD#*/}
export competitions=$1
export allowed_pos=$2
export features=$3
export rankings=$4
export unranked=$5
export output_path=$cwd/output/logistic_regression/$competitions+++$allowed_pos+++$features.csv
export output_stat=$output_path.txt
export model_Rscript=$cwd/lib/model_logistic_regression.R
export Rscript=$cwd/lib/logistic_regression.R

#call python script
python lib/semeval_to_R_input.py

#call R script
Rscript lib/logistic_regression.R > $output_stat

#echo output information for user
cat $output_stat
