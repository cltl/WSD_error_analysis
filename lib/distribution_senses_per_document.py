#import built-in modules
import cPickle
import os
from collections import defaultdict
import argparse

'''
this module loads a matrix saved in ../data/matrices
and converts its structure into:
lemma ->
    pos              -> n
    num_senses       -> int ranging from 1 till endless
    total_occurences -> int total number of instances
    mfs              -> int
    
    senses      ->
        document_id ->
            sense -> [occurences,percentage]
        
then this is written to a csv file

gather stats for approach based on occurences across documents

'''
#argparse

#parse user input
parser = argparse.ArgumentParser(description='Writes distribution of senses across documents to csv file in output/distribution_senses_over_documents/<competition>.csv')
parser.add_argument('-i', dest='competition', help='competition: sval2 | sval3 | sval2007 | sval2010 | sval2013', required=True)
args = parser.parse_args()

#create input_path of matrix
main_dir        = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
input_path      = os.path.join(main_dir,
                               "data",
                               "matrices",
                               args.competition+"_matrix.bin")

output_path     = os.path.join(main_dir,
                               "output",
                               "distribution_senses_over_documents",
                               args.competition+".csv") 


#load matrix
comp,matrix = cPickle.load(open(input_path))

#set defaultdict
data             = defaultdict(dict)
all_document_ids = set()

#loop through matrix
for instance_identifier,info in matrix.iteritems():
    
    #obtain document identifier and lemma
    document_identifier = instance_identifier.split(".")[0]
    all_document_ids.update([document_identifier])
    lemma               = info['lemma']
    pos                 = info['pos']
    num_senses          = info['num_senses']
    
    #update data
    data[lemma]['pos']        = pos
    data[lemma]['num_senses'] = num_senses
    if 'senses' not in data[lemma]:
        data[lemma]['senses'] = {}
    if document_identifier not in data[lemma]['senses']:
        data[lemma]['senses'][document_identifier] = {}
        
    #obtain gold keys 
    gold_keys = info['valid_skeys']
    mfs       = info['MFS']
    if 'mfs' not in data[lemma]:
        data[lemma]['mfs'] = 0
    if mfs == "Yes_MFS":
        data[lemma]['mfs'] +=1
        
    
    #add to dict
    for gold_key in gold_keys:
        
        if gold_key not in data[lemma]['senses'][document_identifier]:
            data[lemma]['senses'][document_identifier][gold_key] = [0.0,0]
        
        data[lemma]['senses'][document_identifier][gold_key][0] += 1
        
#add percentages
    for lemma,info in data.iteritems():
        
        total_occurences = 0
        
        for document_identifier,d in info['senses'].iteritems():
            
            total = sum([value[0] for value in d.itervalues()])
            total_occurences += total
            
            for sense_key,[occ,perc] in d.iteritems():
                perc = occ/total
                data[lemma]['senses'][document_identifier][sense_key][1] = perc
        
        data[lemma]['total_occurences'] = total_occurences
        
#write to file

with open(output_path,"w") as outfile:
    
    headers = ["lemma","pos","num_senses","total_occurences",'mfs',"occurs_in_x_num_docs"]
    for document_identifier in all_document_ids:
        doc_headers =[document_identifier+suffix for suffix in ["_%_predom","_occ_predom","_key_predom"]]
        headers.extend(doc_headers)
        
    outfile.write("\t".join(headers)+"\n")
    
    for lemma,info in data.iteritems():
        
        #obtain pos and num_senses
        pos              = info['pos']
        num_senses       = info['num_senses']
        senses           = info['senses']
        total_occurences = info['total_occurences']
        mfs_count        = info['mfs']
        
        #only write to file is freq is two or more
        if num_senses >= 2:
            occurs_in_x_num_docs = len(senses)
            output = [lemma,pos,num_senses,total_occurences,mfs_count,occurs_in_x_num_docs]
            
            for document_identifier in all_document_ids:
                if document_identifier in senses:
                    
                    highest_key = sorted([(lijst[1],lijst[0],sense_key)
                                          for sense_key,lijst in senses[document_identifier].iteritems()
                                          ], reverse=True)
                    
                    output.extend(highest_key[0])
                else:
                    output.extend(["NA","NA","NA"])
            
            #write to file
            output = [str(item) for item in output]
            outfile.write("\t".join(output)+"\n")
        

#send information for user to std out
print
print "distribution of lemma senses across documents for competition: %s" % args.competition
print "have been written to: " + output_path     














