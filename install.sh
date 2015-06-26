#!/bin/bash

here=$(pwd)

#DATA FOLDER
cd data
git clone https://github.com/rubenIzquierdo/sval_systems
git clone https://github.com/rubenIzquierdo/wsd_corpora
mkdir wordnets
cd wordnets
wget http://wordnetcode.princeton.edu/1.7.1/WordNet-1.7.1.tar.gz
tar xzf WordNet-1.7.1.tar.gz
rm WordNet-1.7.1.tar.gz
mv WordNet-1.7.1/ wordnet-1.7.1

wget http://wordnetcode.princeton.edu/2.1/WordNet-2.1.tar.gz
tar xzf WordNet-2.1.tar.gz
rm WordNet-2.1.tar.gz
mv WordNet-2.1/ wordnet-2.1

wget http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz
tar xzf WordNet-3.0.tar.gz
rm WordNet-3.0.tar.gz
mv WordNet-3.0/ wordnet-3.0
cd ..
cd ..   #BACK TO $here

#EXTLIB
rm -rf $here/extlib 2> /dev/null
mkdir $here/extlib
cd extlib
touch __init__.py
git clone https://github.com/cltl/KafNafParserPy
cd ..   #BACK TO $here

#create matrices (takes a few minutes)
#mkdir -p data/matrices
#python create_data_matrix.py sval2 data/matrices/sval2_matrix.bin > /dev/null 2> /dev/null
#python create_data_matrix.py sval3 data/matrices/sval3_matrix.bin > /dev/null 2> /dev/null
#python create_data_matrix.py semeval2007 data/matrices/sval2007_matrix.bin > /dev/null 2> /dev/null
#python create_data_matrix.py semeval2010 data/matrices/sval2010_matrix.bin
#python create_data_matrix.py semeval2013 data/matrices/sval2013_matrix.bin > /dev/null 2> /dev/null

#create output folder
mkdir -p output/gs_analysis
mkdir -p output/logistic_regression
mkdir -p output/plots
mkdir -p output/mfs_vs_notmfs
mkdir -p output/distribution_senses_over_documents
mkdir -p output/monosemous_errors
mkdir -p output/pos_error