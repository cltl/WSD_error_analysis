from __future__ import division
import subprocess
import os
import cPickle 
from numpy import array 

from scipy.stats.stats import pearsonr

#command 
cmd = "python sense_entropy.py -i {input_folder} -w {resource} -r {reftype} -o {output_folder}"

#competition 1
input_folder  = "/Users/marten/git/WSD_error_analysis/data/wsd_corpora/semeval2013_task12/en"
resource      = "WordNet-3.0"
reftype       = "sense"
output_folder = os.getcwd()
semeval2013   = "/Users/marten/git/WSD_error_analysis/lib/WordNet-3.0_sense"
#subprocess.call(cmd.format(**locals()),shell=True)

#competition 2
input_folder  = "/Users/marten/git/WSD_error_analysis/data/wsd_corpora/semcor3.0"
resource      = "WordNet-eng30"
reftype       = "synset"
output_folder = os.getcwd()
semcor30      = "/Users/marten/git/WSD_error_analysis/lib/WordNet-eng30_synset"
#subprocess.call(cmd.format(**locals()),shell=True)

#vectors
semeval2013 = cPickle.load(open(semeval2013))
semcor30    = cPickle.load(open(semcor30))

v1 = []
v2 = []

for (lemma,pos),info in semcor30.iteritems():
    
    if (lemma,pos) in semeval2013:
        
        d1 = info['senses'].values()
        d2 = semeval2013[(lemma,pos)]['senses'].values()
        
        perc_mfs_2013 = max(d1) / sum(d1)
        perc_mfs_30   = max(d2) / sum(d2)
        
        v1.append(perc_mfs_2013)
        v2.append(perc_mfs_30)

print pearsonr(array(v1),array(v2))


#cosine similarity