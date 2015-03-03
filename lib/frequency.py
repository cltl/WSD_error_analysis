from __future__ import division
import os
import operator
import pickle
#import matplotlib.pyplot as plt
import math


__this_dir__ =  os.path.dirname(os.path.realpath(__file__))

'''
possible sources frequency lists
(1) http://www.kilgarriff.co.uk/BNClists/lemma.al
(2) http://ucrel.lancs.ac.uk/bncfreq/lists/1_1_all_alpha.txt
(3) IMPLEMENTED HERE: http://norvig.com/ngrams/
'''

def get_lemma(token):
    '''
    This method is a very UGLY way to use the internal wordnet lemmatizer,
    which is different from the stemmer and also better.
    NOTE: could be done differently!
    
    @requires: nltk.corpus.wordnet
    
    @type token: string
    @param: token: token to be lemmatised
    
    @rtype: string
    @return: guessed lemma of token
    '''
    export = {}
    for synset in wn.synsets(token):
        for lemma in synset.lemma_names:
            if lemma not in export:
                export[lemma] = 0
            export[lemma]+=1
    sorted_export = sorted(export.iteritems(), key=operator.itemgetter(1),reverse=True)
    return sorted_export[0][0]

def create_norvig_lemma_to_freq(outwrite=False):  
    '''
    method lemmatises unigram freq list from http://norvig.com/ngrams/
    and saves this mapping to "norvig_lemma_freq.txt"
    
    @rtype: dict
    @return: lemmatised mapping from lemma to freq
    ''' 
    from nltk.corpus import wordnet as wn

    d={}
    freqlist = os.path.join(__this_dir__ ,"count_1w.txt")
    with open(freqlist) as infile:
        for line in infile:
            token,freq = line.strip().split("\t")
            try:
                lemma = get_lemma(token)
            except:
                lemma = token
            if lemma not in d:
                d[lemma] = 0
            d[lemma]+=int(freq)
    
    if outwrite:
        with open("norvig_lemma_freq.txt","w") as outfile:
            pickle.dump(d,outfile)
    return d 

def create_freq_dict(method,inspect=False,log_it=False):
    
    '''
    Convert freq of lemma from method create_norvig_lemma_to_freq into relative frequency.
    Two options are available:
    (1) 100% is the most frequent lemma.
    (2) 100% is sum of all frequencies
    
    Proposal:
    (1) I think we should do the 'sum' method
    (2) I do not believe we should do the cross fold method -> inspection_freq_distribution.csv
    because the distribution is so skewed.
    
    @type method: string
    @param method: 'sum','mfs'
    
    @type inspect: [optional] boolean
    @param inspect: if set to True shows graph of all percentages
    
    @type log_it : [optional] boolean
    @param log_it: log the frequencies
    @rtype: dict
    @return: mapping lemma to relative frequency based on method
    '''
    if os.path.isfile("norvig_lemma_freq.txt"):
        lemma_to_freq = pickle.load(open(os.path.join(__this_dir__ ,"norvig_lemma_freq.txt")))
    else:
        lemma_to_freq = create_norvig_lemma_to_freq()
        
    if method == "sum":
        total = sum(lemma_to_freq.itervalues())
    if method == "mfs":
        total = max(lemma_to_freq.itervalues())
    
    
    for lemma,freq in lemma_to_freq.iteritems():
        if log_it:
            lemma_to_freq[lemma] = math.log(freq)
        else:
            lemma_to_freq[lemma] = (freq/total)*100
    
    if inspect:
        percentages = [round(perc,2) for perc in lemma_to_freq.itervalues()]
        values = sorted([(perc_class,percentages.count(perc_class)) for perc_class in set(percentages)])
        x,y = zip(*values)
        plt.plot(x,y)
        plt.savefig('inspection_freq_distribution.pdf')
        with open('inspection_freq_distribution.csv','w') as outfile:
            outfile.write("perc_class\tfreq\n")
            for perc_class,freq in values:
                outfile.write("%s\t%s\n" % (perc_class,freq))
    return lemma_to_freq

 
##create_freq_dict('sum', inspect=True, log_it=False)
