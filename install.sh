#!/bin/bash

here=$(pwd)

#DATA FOLDER
rm -rf $here/data 2> /dev/null
mkdir $here/data
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



