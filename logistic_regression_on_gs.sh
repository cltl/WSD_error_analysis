
#check if enough arguments are passed, else print usage information
if [ $# -eq 0 ];
then
    echo
    echo "Usage:                  : $0 competition allowed_pos features"
    echo
    echo "competition            : Options are sval2 sval3 sval2007 sval2010 sval2013"
    echo "allowed_pos             : concatenated by underscore the pos you want\
    to include. Options are: n, v, a, r, u."
    echo "features                : concatenated by '---' the features you want\
    to include in the analysis. Options are: \
    token based : len_sentence copula  avg_num_senses_in_sentence \
    type based  : num_senses pos rel_freq total_occurences occurs_in_x_num_docs"
    echo
    echo 'example of call:'
    echo 'logistic regression is performed with the explanatory variable being \
    whether or not the gold sense is the most frequent sense or not.'
    echo 'bash logistic_regression_on_gs.sh sval2013 n num_senses---pos'
    echo
    echo "the output of the logistic regression will be shown in the terminal"
    exit -1;
fi

#assign command line arguments to variables and obtain basename
export cwd=/${PWD#*/}
export competition=$1
export allowed_pos=$2
export features=$3

#define paths
export output_path=$cwd/output/logistic_regression/gs_$competition+++$allowed_pos+++$features.csv
export distribution_senses_csv=$cwd/output/distribution_senses_over_documents/$competition.csv

export output_stat=$output_path.txt
export model_Rscript=$cwd/lib/model_logistic_regression.R
export Rscript=$cwd/lib/logistic_regression.R

#call python script
python lib/distribution_senses_per_document.py

#call R script
Rscript lib/logistic_regression.R > $output_stat

#echo output information for user

#distribution senses per document
#echo 'distribution of senses per document can be found at:'
#echo $distribution_senses_csv
#echo
#logistic regression output
#echo 'output logistic regression can be found at:'
#echo $output_stat
#echo 
cat $output_stat

#to latex table
python lib/latex_tables.py -i $output_stat -t logistic_regression
echo 
echo $output_stat.tex