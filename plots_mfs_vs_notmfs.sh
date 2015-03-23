#assign command line arguments to variables
export cwd=/${PWD#*/}

#rm and create output folder
export output_folder=$cwd/output/mfs_vs_notmfs
export output_pdf=$output_folder/plot.pdf

#call python script
python lib/mfs_vs_notmfs.py

#echo output information to user
echo
echo 'output folder can be found here:'
echo $output_folder
echo
echo 'path to plot:'
echo $output_pdf
