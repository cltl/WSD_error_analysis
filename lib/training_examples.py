import os
import mfs_dict_utils
from lxml import etree 
from collections import defaultdict
import cPickle

data = {}

input_folder = os.environ['input_dir']

for naf_file in mfs_dict_utils.path_generator(input_folder,".naf"):
    doc = etree.parse(naf_file)
    for term_el in doc.iterfind('terms/term'):
        lemma = term_el.get('lemma')
        
        ext_refs_el = term_el.find('externalReferences')
        if ext_refs_el is not None:
            sense_number = ext_refs_el.find("externalRef[@resource=\"WordNet-eng30\"]").get('reference')
            synset = ext_refs_el.find("externalRef[@reftype=\"lexical_key\"]").get('reference')
            
            if sense_number != '1':
                sense_number = 'reste'
            
            if lemma not in data:
                data[lemma] = defaultdict(int)

            data[lemma][sense_number] += 1
            data[lemma]['total'] += 1
            
            if data[lemma]['1'] != 0:
                data[lemma]['mfs_perc'] = (data[lemma]['1']/data[lemma]['total'])
            else:
                data[lemma]['mfs_perc'] = 0.0

total = sum([data[lemma]['total'] for lemma in data.iterkeys()])
first_senses = sum([data[lemma]['1'] for lemma in data.iterkeys()])
perc_first_senses = float(first_senses)/total

mfs_percs = [data[lemma]['mfs_perc'] for lemma in data.iterkeys()]
av_mfs_perc = float(sum(mfs_percs))/len(mfs_percs)
print(first_senses,total,perc_first_senses,av_mfs_perc)
                
            
                
            

            