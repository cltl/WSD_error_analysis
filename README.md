#WSD Error analysis#

This repo provides various ways to analyse system submissions to wsd competitions.

##Installation##
* Clone this repository:
    * cd repository_folder
    * see INSTALL.md (which is placed in the same folder as this README) for information about dependencies
    * bash install.sh (takes about 5 minutes)

##USAGE##
* [Python 2.7] run `bash error_analysis.sh` to create the graphs and tables
* [Python 3.6] run `bash trends.sh` to create the plots for the F1 trends
* other .sh files: 
    * call each file and the information about how to use it will be send to stdout
* [Python 3.6] run `wn_explanation/WordNet_explanation.ipynb` to create the image used to explain the WordNet structure

##In order to recreate data matrices (this is already done in install.sh)##
run: python create_data_matrix.py sval2|sval3|semeval2007|semeval2010|semeval2013 matrix_filename

##Contact##
* Ruben Izquierdo Bevia
* ruben.izquierdobevia@vu.nl
* http://rubenizquierdobevia.com/
* Free University of Amsterdam

***

* Marten Postma
* m.c.postma@vu.nl
* http://martenpostma.com/
* Free University of Amsterdam
