export cwd=/${PWD#*/}

#gold standard stats

function gs_stats () {

#do analysis
for com in sval2 sval3 sval2007 sval2010 sval2013; 
do 
	bash provide_stats_gs.sh $com
done

#convert to latex table
python lib/latex_tables.py -i $cwd/output/gs_stats -t 'gs_stats'
cat $cwd/output/gs_stats/gs_stats_table.tex

}

function mfs_plot () { 

#TODO: fix mfs sval2010 (ask ruben how he determined mfs)
bash plots_mfs_vs_notmfs.sh

}


function plots_gold_standards () {

#plot graph
bash plots_gold_standards.sh sval2_sval3_sval2007_sval2010_sval2013 n_v_a_r

#state which lemma are used on a document level in more than one meaning
head output/gs_analysis/sval2_sval3_sval2007_sval2010_sval2013+++n_v_a_r_u/document.csvstats.csv
}


function logistic_regression_on_gs () {

#do analysis
for com in sval2 sval3 sval2007 sval2010 sval2013; 
do 
	bash logistic_regression_on_gs.sh $com n_v_r_a num_senses---occurs_in_x_num_docs
	bash logistic_regression_on_gs.sh $com n_v_r_a len_sentence---avg_num_senses_in_sentence---num_senses---pos---rel_freq---total_occurences---occurs_in_x_num_docs
done


}

function monosemous_errors () {

bash monosemous_errors.sh sval2_sval3_sval2007_sval2010_sval2013 1000 yes
bash monosemous_errors.sh sval2_sval3_sval2007_sval2010_sval2013 1 no

#best systems tend to use better pos systems

}
#####################################################
#run all functions and send output or path to stdout


#Section X 
#gs_stats

#Section X
#mfs_plot

#Section X
#plots_gold_standards

#Section X
#logistic_regression_on_gs

#Section X
monosemous_errors


