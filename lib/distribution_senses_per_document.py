#import built-in modules
import cPickle
import os
from collections import defaultdict

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
#parse variables as defined in ../logistic_regression_on_gs.sh
competition=os.environ['competition']

#create input_path of matrix
main_dir        = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

input_path      = os.path.join(main_dir,
                               "data",
                               "matrices",
                               competition+"_matrix.bin")

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

with open(os.environ['distribution_senses_csv'],"w") as outfile:
    
    headers = ["lemma","pos","num_senses","total_occurences",'mfs',"occurs_in_x_num_docs"]
    for document_identifier in all_document_ids:
        doc_headers =[document_identifier+suffix for suffix in ["_%_predom","_occ_predom","_key_predom"]]
        headers.extend(doc_headers)
        
    outfile.write("\t".join(headers)+"\n")
    
    for lemma,info in data.iteritems():
        
        #obtain pos and num_senses
        pos                          = info['pos']
        num_senses                   = info['num_senses']
        senses                       = info['senses']
        total_occurences             = info['total_occurences']
        mfs_count                    = info['mfs']
        occurs_in_x_num_docs         = len(senses)
        info['occurs_in_x_num_docs'] = occurs_in_x_num_docs
        
        #only write to file is freq is two or more
        if num_senses >= 2:
             
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
        
#create input for R

allowed_pos  = os.environ['allowed_pos'].split('_')
features     = os.environ['features'].split("---")

#remove pos from feature list if only one value inserted
if len(allowed_pos) == 1:
    if 'pos' in features:
        features.remove('pos')
    
#read model R script
with open(os.environ["model_Rscript"]) as infile:
    raw = infile.read()

#change raw with experiment settings
raw       = raw.replace("CSV_INPUT",os.environ['output_path'])
variables = " + ".join(features)
raw       = raw.replace("VARIABLES",variables)
with open(os.environ['Rscript'],"w") as outfile:
    outfile.write(raw)
    
#create R_input script
with open(os.environ['output_path'],"w") as outfile:
            
    #write headers to file
    headers = ['correct'] + features
    outfile.write(",".join(headers)+"\n")
    
    #loop
    for instance_identifier,info in matrix.iteritems():
        
        output = []
        #add features
        for feature in features:
            if feature in info:
                value = info[feature]
                
                #in the case of rel_freq, unknown is set to -1, here I change the default to 0
                if value == -1:
                    value = 0
                output.append(value)
            else:
                lemma = info['lemma']
                output.append(data[lemma][feature])
        
        #mfs
        explanatory_variable = 0
        if info['MFS'] == "Yes_MFS":
            explanatory_variable = 1
        output.insert(0,explanatory_variable)
        
        #write to file
        output = [str(item) for item in output]
        outfile.write(",".join(output)+"\n")
