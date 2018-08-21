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
output.append(("# instances",num_tokens))

#pos
pos = set( value['pos'] 
           for value in d.itervalues()
           if value['pos']  != 'u')
pos = " ".join(pos)
output.append(("POS",pos))

#types
num_types = len(set( value['lemma'] for value in d.itervalues() ))
output.append(("# lemmas",num_types))

#type token ratio
type_token_ratio = float(num_types)/float(num_tokens)
type_token_ratio = round(type_token_ratio,2)
output.append(("type token ratio",type_token_ratio))

# meanings
meanings = set()
for id_, instance_info in d.iteritems():

    pos = instance_info['pos']
    gold_keys = instance_info['valid_skeys']

    if competition == 'sval2010':
        meanings.update(gold_keys)
    else:
        for key, offset, senserank in instance_info['list_senses']:

            if key in gold_keys:
                ili = offset + '-' + pos
                meanings.add(ili)

#output.append(('| {gold meanings} |', len(meanings)))








#document
num_docs = len( set( key.split(".")[0] for key in d.iterkeys() ))
output.append(("# docs",num_docs))

with open(output_path,"w") as outfile:
    for label,value in output:
        outfile.write("%s\t%s\n" % (label,value))
