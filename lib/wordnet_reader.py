import os
from collections import defaultdict

class wordnet_reader:
    def __init__(self,path_to_wordnets):
        self.path_to_wordnets = path_to_wordnets
        
    def get_path_to_file(self,this_file,this_version):
        path_to_file = None
        if this_version in ['171','1.7.1','wn171']:
            path_to_file = os.path.join(self.path_to_wordnets,'wordnet-1.7.1','dict',this_file)
        else:
            path_to_file = None
        return path_to_file
    
    def convert_int_pos_to_char(self, int_pos):
        """
        Converts the pos label integer of WN in a char
        """
        this_pos = None
        if int_pos in ['1']:
            this_pos = 'n'
        elif int_pos in ['2']:
            this_pos = 'v'
        elif int_pos in ['3','5']:
            this_pos = 'a'
        elif int_pos in ['4']:
            this_pos = 'r'
        else:
            this_pos = 'u'
        return this_pos
    
    def get_index_lemma_to_senses(self,wn_version):
        """
        Creates and index to store for each (lemam,pos) all the possible senses of that word (and sensekeys and synsets)
        index[(house,n)] = [(house%1...,001323242,1), (house%1xxxx, 02341212,2)...]
        """
        path_to_file = self.get_path_to_file('index.sense', wn_version)
        if path_to_file is None:
            print>>sys.stderr,'Error, version for Wordnet %s not known' % this_version
            
        index = defaultdict(list)
        fd = open(path_to_file,'r')
        for line in fd:
            fields = line.strip().split()
            if len(fields) == 4:
                sensekey,synset,sense,freq = fields
                p = sensekey.find('%')
                this_lemma = sensekey[:p]
                this_int_pos = sensekey[p+1]
                this_pos = self.convert_int_pos_to_char(this_int_pos)
                index[(this_lemma,this_pos)].append((sensekey, synset,sense))
        fd.close()
        return index