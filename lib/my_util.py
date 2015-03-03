import os

def get_naf_filename_for_token(this_folder,corpus,token_id):
    if corpus == 'sval2':   ## Token ids are like: d00.s32.t19 where the first part is the doc id
        doc_id = token_id.split('.')[0]
        naf_filename = os.path.join(this_folder,'data','wsd_corpora','senseval2',doc_id+'.naf')
    elif corpus == 'sval3':
        doc_id = token_id.split('.')[0]
        naf_filename = os.path.join(this_folder,'data','wsd_corpora','senseval3',doc_id+'.naf')
    elif corpus == 'semeval2007':
        doc_id =  token_id.split('.')[0]
        naf_filename = os.path.join(this_folder,'data','wsd_corpora','semeval2007_task17_allwords',doc_id+'.naf')
    elif corpus == 'semeval2010':
        doc_id =  token_id.split('.')[0]
        naf_filename = os.path.join(this_folder,'data','wsd_corpora','semeval2010_task17',doc_id+'.naf') 
    elif corpus == 'semeval2013':
        doc_id =  token_id.split('.')[0]
        naf_filename = os.path.join(this_folder,'data','wsd_corpora','semeval2013_task12','en',doc_id+'.naf') 
    return naf_filename


def get_freqclass_of_freq(relative_freq):
    '''
    Maps relative_freq to frequency class
    
    @type relative_freq : float
    @param relative_freq: relative freq (from approaching zero to 100 in theory)
    
    we have defined three relative frequency classes:
    (1) low      : < 0.01
    (2) middle   : >= 0.01 and < 0.05
    (3) high     : >= 0.05
    '''
    freq_class = None
    if relative_freq < 0.01:
        freq_class = "low"
    else:
        if relative_freq < 0.05:
            freq_class = "middle"
        else:
            freq_class = "high"
    return freq_class