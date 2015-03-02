#!/usr/bin/env python


from lib import sval_systems_reader, wordnet_reader


#import sval_util
import os
import cPickle
import sys
from KafNafParserPy import KafNafParser
from collections import defaultdict
#from frequency import create_freq_dict

os.environ['LC_ALL'] = 'en_US.UTF-8'
__this_dir__ =  os.path.dirname(os.path.realpath(__file__))

wn_version = {}
wn_version['sval2'] = '1.7.1'

def load_copula_skeys(corpus_id):
    filename = None
    if corpus_id == 'sval2':
        filename = 'copula_sense_keys.wn171.txt' 
    if corpus_id == 'sval3':
        filename = 'copula_sense_keys.wn171.txt' 
    else:
        pass
    
    copula_skeys = set()
    if filename is not None:
        fic = open(filename)
        for line in fic:
            copula_skeys.add(line.strip())
        fic.close()
    return copula_skeys
        
    

def get_polysemy_class(num_senses):
    """
    Converts the number of senses (integer) in several ranges
    """
    polysemy_class = None
    if num_senses == 0:
        polysemy_class = '0'
    elif num_senses == 1:
        polysemy_class = 'mono'
    elif num_senses < 5:
        polysemy_class = 'low_polysemy'
    elif num_senses < 15:
        polysemy_class = 'medium_polysemy'
    elif num_senses < 30:
        polysemy_class = 'high_polysemy'
    else:
        polysemy_class = 'very_high_polysemy'
    return polysemy_class
    

def get_mappings_and_sentences(naf_obj):
    """
    Returns three mappings or data structures from the naf obj
    1) A mapping from the senseval id to the NAF id (reading the external references)
    2) A mapping from the naf token id to the sentence identifier
    3) A dictionary where the key is the sentence identifier and the values the list of (token,token_id)
    """
    map_sval_id_naf_id = {}
    for term in naf_obj.get_terms():
        for ext_ref in term.get_external_references():
            if ext_ref.get_reftype() == 'original_id':
                #if ext_ref.get_resource() in ['original_corpus_id','SemEval2010_task17', 'SemEval2010_task17']:
                map_sval_id_naf_id[ext_ref.get_reference()] = term.get_span().get_span_ids()[0]

    ## In naf_token_id we have the naf token identifier
    sentences = defaultdict(list)
    sent_for_tokenid = {}
    token_for_tokenid = {}
    num_sent = 0
    previos_sent = None
    for token in naf_obj.get_tokens():
        sent = token.get_sent()
        if previos_sent is not None and sent != previos_sent:
            num_sent += 1
        previos_sent = sent
        value = token.get_text()
        this_id = token.get_id()
        sentences[sent].append((value,this_id))
        sent_for_tokenid[this_id] = (sent,num_sent)
        token_for_tokenid[this_id] = value
    ##
    return map_sval_id_naf_id, sent_for_tokenid, sentences, token_for_tokenid

def create_data_matrix(corpus,output_file):
    """
    Creates the data matrix for a given corpus identifier, and stores the result in the given
    file
    @param corpus: the identifier for the corpus (sval2,sval3...)
    @type corpus: string
    
    @param output_file: the output filename
    @type corpus: string
    """
    key = {}
    #key is a dict key[tokenid] = [sensekey1,senseky2/..]
    my_reader = sval_systems_reader(os.path.join(__this_dir__,'data','sval_systems'))
    for token_id, gold_labels in my_reader.get_gold_id_and_labels(corpus):
        key[token_id] = gold_labels
    
    data_matrix = {}

    my_wn_reader = wordnet_reader(os.path.join(__this_dir__,'data','wordnets'))
    index_lemma_pos_to_senses = my_wn_reader.get_index_lemma_to_senses(wn_version[corpus])
    sys.exit(0)

    #This will store the mapping (lemma) --> frequency
    lemma_to_freq = create_freq_dict('sum', inspect=False, log_it=False)
    
    #Set of copula skyes
    copula_skeys = load_copula_skeys(corpus)
    
    number_tokens_in_sentence = defaultdict(int)
    total_senses_in_sentence = defaultdict(int)
    
    # We will store here in memory the naf objects, so we don't need to parse more than once each file
    naf_objects = {}
    # Get the information for each token identifier
    for token_id, skeys in key.items():
        ## The sentence where the token appears
        naf_filename = sval_util.get_naf_filename_for_token(corpus,token_id)
        map_sval_id_naf_id = sent_for_tokenid = sentences = token_for_tokenid = None
        if naf_filename not in naf_objects:
            naf_obj = KafNafParser(naf_filename)
            map_sval_id_naf_id, sent_for_tokenid, sentences,token_for_tokenid = get_mappings_and_sentences(naf_obj)
            naf_objects[naf_filename] = (map_sval_id_naf_id, sent_for_tokenid, sentences,token_for_tokenid)
        else:
            map_sval_id_naf_id, sent_for_tokenid, sentences,token_for_tokenid = naf_objects[naf_filename]
           
        naf_token_id = map_sval_id_naf_id[token_id]
        value_token = token_for_tokenid[naf_token_id]
        
        data_for_token = {}

        
        ##The lemma ########
        lemma = pos = ''
        if corpus == 'sval2010':
            guessed_skey,lemma,guessed_sense,d  = sval_util.get_lemma_for_ili(skeys[0],corpus,value_token)
            pos = skeys[0][-1]
        else:
            lemma = sval_util.get_lemma_for_sensekey(skeys[0])
            pos = sval_util.get_pos_for_sensekey(skeys[0])
             
        data_for_token['pos'] = pos
        data_for_token['lemma'] = lemma
        ############################


        ## Copula skeys  ###
        
        if len(set(skeys) & copula_skeys) != 0:
            data_for_token['copula'] = 'copula.yes'
        else:
            data_for_token['copula'] = 'copula.no'
            
        
        ## Polysemy class #########
        list_skey_syn_sense = index_lemma_pos_to_senses[(lemma,pos)]
        num_senses = len(list_skey_syn_sense)
        polysemy_class = get_polysemy_class(num_senses)
        data_for_token['polysemy_class'] = polysemy_class
        data_for_token['num_senses'] = num_senses
        data_for_token['list_senses'] = list_skey_syn_sense
        # We check also if any of the valid skeys corresponds to the sense 1
        is_most_frequent_sense = 'No_MFS'
        if corpus == 'sval2010':
            if guessed_sense == '1':
                is_most_frequent_sense = 'Yes_MFS'
        else:
            for sensekey, synset,sense in list_skey_syn_sense:
                if sense=='1' and sensekey in skeys:
                    is_most_frequent_sense = 'Yes_MFS'
                    break
        data_for_token['MFS'] = is_most_frequent_sense
        ############################
  
  

            
        this_sentence, num_sentence = sent_for_tokenid[naf_token_id]
        sentence = ''
        for value, this_id in sentences[this_sentence]:
            if this_id == naf_token_id:
                sentence+='##'+value+'## '
            else:
                sentence+=value+' '
            
        data_for_token['sentence'] = sentence.strip()
        data_for_token['len_sentence'] = len(sentences[this_sentence])
        data_for_token['num_sentence'] = str(num_sentence)
        #######################################

        ## For the average number of senses per 
        #######################################
        # 1) Obtain the sentence identifier
        sentence_identifier = None 
        doc_sen_tok = token_id.split('.')
        sentence_identifier = doc_sen_tok[0]+'.'+doc_sen_tok[1]
        data_for_token['sentence_identifier'] = sentence_identifier
        
        number_tokens_in_sentence[sentence_identifier] += 1
        total_senses_in_sentence[sentence_identifier] += num_senses
        
        # The frequency class
        relative_frequency = lemma_to_freq.get(lemma,-1)
        frequency_class = sval_util.get_freqclass_of_freq(relative_frequency)
        data_for_token['rel_freq'] = relative_frequency
        data_for_token['freq_class'] = frequency_class
        #######################################
        if corpus == 'sval2010':
            data_for_token['valid_skeys'] = [guessed_skey]
        else:
            data_for_token['valid_skeys'] = skeys
                
        # Store the data for this token
        data_matrix[token_id] = data_for_token
        
    for token in data_matrix.keys():
        sent_id = data_matrix[token]['sentence_identifier']
        data_matrix[token]['avg_num_senses_in_sentence'] = total_senses_in_sentence[sent_id]*1.0/number_tokens_in_sentence[sent_id]
        data_matrix[token]['num_test_token_in_sentence'] =  number_tokens_in_sentence[sent_id]
        
        
    fout = open(output_file,'wb')
    my_data = (corpus,data_matrix)
    cPickle.dump(my_data, fout, protocol=0)
    fout.close()
    print>>sys.stderr,'  First tokens as example'
    import pprint
    pprint.pprint(data_matrix.items()[:20])
    
    print>>sys.stderr, 'Data matrix for',corpus,'saved in',fout.name
    print>>sys.stderr, 'Possible keys for experiments:'
    for key in data_for_token.keys():
        print>>sys.stderr,'   ',key
    print>>sys.stderr
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print>>sys.stderr,'Usage:',sys.argv[0]+' corpus_name matrix_filename'
        sys.exit(-1)
    
    create_data_matrix(sys.argv[1],sys.argv[2])
    print 'File for corpus',sys.argv[1],'in',sys.argv[2]