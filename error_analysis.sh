export cwd=/${PWD#*/}

#gold standard stats

function gs_stats () {

#do analysis
for com in sval2 sval3 sval2007 sval2010 sval2013;
do
	result=$(bash provide_stats_gs.sh $com)
done

#convert to latex table
python lib/latex_tables.py -i $cwd/output/gs_stats -t 'gs_stats'
echo
cat $cwd/output/gs_stats/gs_stats_table.tex

}

function mfs_plot () {

echo '% created with function mfs_plot in clin2015.sh'
bash plots_mfs_vs_notmfs.sh

}


function plots_gold_standards () {

echo
echo '% created with function plots_gold_standards in clin2015.sh'
echo
#plot graph
bash plots_gold_standards.sh sval2_sval3_sval2007_sval2010_sval2013 n_v_a_r

#state which lemma are used on a document level in more than one meaning
head output/gs_analysis/sval2_sval3_sval2007_sval2010_sval2013+++n_v_a_r_u/document.csvstats.csv
}


function logistic_regression_on_gs () {

echo '% created with function logistic_regression_on_gs in clin2015.sh'
#do analysis
#for com in sval2 sval3 sval2007 sval2010 sval2013;
#do
#	bash logistic_regression_on_gs.sh $com n_v_r_a num_senses---occurs_in_x_num_docs
#	bash logistic_regression_on_gs.sh $com n_v_r_a len_sentence---avg_num_senses_in_sentence---num_senses---pos---rel_freq---total_occurences---occurs_in_x_num_docs
#done

bash logistic_regression_on_gs.sh sval2013 n_v_r_a num_senses---occurs_in_x_num_docs---rel_freq---total_occurences

}

function logistic_regression () {

echo '% created with function logistic_regression on clin2015.sh'
echo
#do analysis
bash logistic_regression.sh sval2_sval3_sval2007_sval2010_sval2013 n_v_r_a num_senses---copula---rel_freq---avg_num_senses_in_sentence---MFS 1 no
bash logistic_regression.sh sval2_sval3_sval2007_sval2010_sval2013 n_v_r_a num_senses---copula---rel_freq---avg_num_senses_in_sentence---MFS 50 yes

#-num_senses is significant for all settings
#-for best systems: posv is not significant, it is for all
#-relevant freq is positively significant
#-MFSyes is highly significant for all
#-avg_num_senses_in_sentence is significant for all, not for best systems.


}

function monosemous_errors () {

export average=$(bash monosemous_errors.sh sval2_sval3_sval2007_sval2013 1000 yes)
export top=$(bash monosemous_errors.sh sval2_sval3_sval2007_sval2013 1 no)
python lib/monosemous_errors_plotting.py

echo
echo '% created with function monosemous_errors in clin2015.sh'
echo 'monosemous errors plot can be found here:'
echo $cwd/output/monosemous_errors/monosemous_errors.pdf
#best systems tend to use better pos systems

}

function pos_errors () {

echo
echo '% created with function pos_errors in clin2015.sh'
bash precision_plotting.sh sval2_sval3_sval2007_sval2010_sval2013 pos 1 no
}

function freq_class () {

echo
echo '% created with function polysemy_errors in clin2015.sh'
bash precision_plotting.sh sval2_sval3_sval2007_sval2010_sval2013 freq_class 1 no
}

#####################################################
#run all functions and send output or path to stdout

#echo
#echo 'Gold standard stats'
#gs_stats

#echo
#echo 'Monosemous errors'
#monosemous_errors

#features that were not significant:
	#pos
	#len\_sentence
#echo
#echo 'Logistic regression'
#logistic_regression
#echo

#echo
echo 'mfs plot'
mfs_plot

#echo
#echo 'Part of speech errors'
#echo
#pos_errors

#echo
#echo 'gold standard plots'
#plots_gold_standards

#echo
#echo 'Logistic regression on gold standards'
#logistic_regression_on_gs
