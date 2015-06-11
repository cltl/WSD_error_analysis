#import built-in modules
import argparse
import glob
from collections import defaultdict
import cPickle
import os
from math import log

#import external modules
import mfs_dict_utils as utils
from lxml import etree
from nltk.corpus import wordnet as wn
'''
goal of this module is to
(1) loop through semcor
(2) count for every (lemma,pos) the sense distribution
(3) calculate normalised sense entropy for each (lemma,pos)
'''

__author__     = "Marten Postma"
__license__    = "Apache 2.0"
__version__    = "1.0"
__maintainer__ = "Marten Postma"
__email__      = "martenp@gmail.com"
__status__     = "production"

#parse arguments
parser = argparse.ArgumentParser(description='Load sense entropy from SemCor')

parser.add_argument('-i',   dest='input_folder',   help='folder with naf files (to semcor 1.6 or semcor 3.0)',  required=True)
parser.add_argument('-w',   dest='resource',       help='WordNet-eng16 | WordNet-eng30',                        required=True)
parser.add_argument('-r',   dest='reftype',        help="lexical_key | synset",                                 required=True)
parser.add_argument('-o',   dest="output_folder",  help="basename will be resource_reftype",                    required=True)
parser.add_argument('--ili',  dest="ili", type=bool, help="if 'ili' is added at the end of the call, the synset references will be converted to ili definitions")

args = parser.parse_args()


def entropy(list_of_floats,
            normalized=False,
            base=2):
    '''
    given a list of floats, the entropy is returned
    
    >>> entropy([0.2,0.2,0.2,0.2,0.2],normalized=True)
    1.0
    
    >>> entropy([0.2,0.2,0.2,0.2,0.2],normalized=False)
    2.321928094887362
    
    >>> entropy([])
    0.0
    
    @requires: math.log 
    
    @type  list_of_floats: list
    @param list_of_floats: list of floats. for example [0.5,0.5]
    
    @type  normalized: bool
    @param normalized: if True, entropy is normalized from 0 to 1 (default
    is False)
    
    @type  base: int
    @param base: base of log (default is 2)

    @rtype: float
    @return: normalized entropy. 0.0 is returned if list is empty
    '''
    #if empty list, return 0.0:
    if not list_of_floats:
        return 0.0 
    
    #calculate Shannon Entropy (S) = -Si(piLnpi)
    S = -1.0 * sum([ (p * ( log(p,base) ) )
                  for p in list_of_floats])
    
    #normalize if needed
    if normalized:
        len_list_of_floats = len(list_of_floats)
        if len_list_of_floats == 1:
            S = 0.0
        else:
            S = S/log(len_list_of_floats,2)
    
    return S

#set data
sense_freq = defaultdict(dict)

#set string to external references elements in naf
path_to_ext_ref_els = "/".join(["terms",
                                "term",
                                "externalReferences",
                                "externalRef"
                                ])

#loop through naf files
for naf_file in utils.path_generator(args.input_folder,".naf"):
    
    #parse naf file
    doc = etree.parse(naf_file)
    
    #loop through it
    for ext_ref_el in doc.iterfind(path_to_ext_ref_els):
        
        #check parameters settings
        attrib = ext_ref_el.attrib
        if all([attrib['resource'] == args.resource,
                attrib['reftype']  == args.reftype
                ]):
            #obtain reference
            reference = attrib['reference']
            
            #convert it if needed by args.ili
            if args.ili:
                reference = reference.replace("eng","ili-")

            #obtain pos,lemma
            pos       = reference[-1]
            lemma     = ext_ref_el.getparent().getparent().get("lemma")
            lemma_pos = (lemma,pos)
            
            #add to dict
            if lemma_pos not in sense_freq:
                sense_freq[lemma_pos]["senses"] = defaultdict(int)
            sense_freq[lemma_pos]["senses"][reference] += 1

#calculate mfs, sense entropy
for (lemma,pos),info in sense_freq.iteritems():
    
    mfs = utils.mfs(info['senses'])
    
    sense_freq[lemma,pos]['mfs'] = mfs

    #add 1 for all missing senses (dummy values)
    freqs      = info['senses'].values()
    num_senses = len(wn.synsets(lemma,pos=pos))
     
    for dummy in xrange(num_senses - len(freqs)):
        freqs.append(1)
    
    #convert counts to percentages
    total = float(sum(freqs))
    percs = [freq/total for freq in freqs]
    
    #add sense entropy
    sense_entropy = entropy(percs,normalized=True)
    info['entropy'] = sense_entropy
    
#write output

if args.ili:
    args.reftype = "ili"
    
output_path = os.path.join(args.output_folder,
                           args.resource+"_"+args.reftype)
with open(output_path,"w") as outfile:
    cPickle.dump(sense_freq, outfile, protocol=0)
    
print
print "the sense frequency and entropy dict for:"
print "resource: %s" % args.resource
print "reftype:  %s" % args.reftype
print
print "can be found here:"
print output_path
print
print 'the cPickle object has the following structure:'
print '''
'(lemma,pos)':
        -> 'mfs':    : list of one or more senses with the highest freq in SemCor version
        -> 'senses'  : dictionary mapping from reference (str) to count (int)
        -> 'entropy' : entropy of senses
'''