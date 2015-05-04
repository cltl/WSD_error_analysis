#import general modules
import cPickle
import os

#modules in this cwd
import utils


#obtain exp settings from os.environ and load dict
competition = os.environ['competition']
output_path = os.environ['output_path']
com_to_bin  = utils.mapping_competition_to_bin()
path_bin    = com_to_bin[competition]
com,d       = cPickle.load(open(path_bin))
output      = []

#num instances
num_tokens = len(d)
output.append(("num_tokens",num_tokens))

#pos
pos = set( value['pos'] 
           for value in d.itervalues()
           if value['pos']  != 'u')
pos = " ".join(pos)
output.append(("pos",pos))

#types
num_types = len(set( value['lemma'] for value in d.itervalues() ))
output.append(("num_types",num_types))

#type token ratio
type_token_ratio = float(num_types)/float(num_tokens)
type_token_ratio = round(type_token_ratio,2)
output.append(("type_token_ratio",type_token_ratio))

#document
num_docs = len( set( key.split(".")[0] for key in d.iterkeys() ))
output.append(("num_docs",num_docs))

with open(output_path,"w") as outfile:
    for label,value in output:
        outfile.write("%s\t%s\n" % (label,value))
