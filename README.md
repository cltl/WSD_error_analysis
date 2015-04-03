#WSD Error analysis#

This repo provides various ways to analyse system submissions to wsd competitions.

##Installation##
* Clone this repository:
    * cd repository_folder
    * see INSTALL.md (which is placed in the same folder as this README) for information about dependencies
    * bash install.sh (takes about 5 minutes)

##USAGE##
* logistic regression:
    * run bash logistic_regression.sh for more information about how to use the script
* plots gold standards:
    * run plots_gold_standards.sh for more information about how to use the script
* basic stats gold standards:
    * run provide_stats_gs.sh for more information about how to use the script
* plots_mfs_vs_notmfs
    * run plots_mfs_vs_notmfs.sh for more information
* lib/distribution_senses_per_document.py
    * run python lib/distribution_senses_per_document.py for more information

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
