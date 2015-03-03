import os
import sys
from collections import defaultdict
from subprocess import Popen, PIPE


class wordnet_reader:
    def __init__(self,path_to_wordnets):
        self.path_to_wordnets = path_to_wordnets
        
    def get_path_to_file(self,this_file,this_version):
        path_to_file = None
        if this_version in ['171','1.7.1','wn171']:
            path_to_file = os.path.join(self.path_to_wordnets,'wordnet-1.7.1','dict',this_file)
        elif this_version in ['21','2.1','wn21']:
            path_to_file = os.path.join(self.path_to_wordnets,'wordnet-2.1','dict',this_file)
        elif this_version in ['30','3.0','wn30']:
            path_to_file = os.path.join(self.path_to_wordnets,'wordnet-3.0','dict',this_file)
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
            print>>sys.stderr,'Error, version for Wordnet %s not known' % wn_version
            
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
    
    def levenshtein(self, s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
     
        return v1[len(t)]

    def get_lemma_for_ili(self,ili_record,corpus,value_token, wn_version):
        index_file = self.get_path_to_file('index.sense', wn_version)
        fields = ili_record.split('-')
        synset = fields[2]
        from subprocess import Popen, PIPE
        cmd = "grep '%s' %s" % (synset,index_file)
        proc = Popen(cmd,stdin=PIPE, stdout=PIPE, shell=True)
        out,err = proc.communicate()
        list_values = []
        for line in out.splitlines():
            fields = line.strip().split()
            skey = fields[0]
            lemma = skey[:skey.find('%')]
            synset = fields[1]
            sense = fields[2]
            d = self.levenshtein(lemma, value_token)
            list_values.append((skey,lemma,sense,d))
        best = sorted(list_values, key=lambda t: t[3])[0]
        return best ##(skey,lemma,sense,distance)
    
    def get_lemma_for_sensekey(self, skey):
        """
        Gets the lemma out of a sensekey
        """
        this_lemma = ''
        if skey == 'U':
            this_lemma = 'u'
        else:
            p = skey.rfind('%')
            this_lemma = skey[:p]
        return this_lemma
    
    def get_pos_for_sensekey(self, skey):
        """
        Gets the pos char label for a given sense key
        """
        this_pos = ''
        if skey == 'U':
            this_pos = 'u'
        else:
            p = skey.rfind('%')
            int_pos = skey[p+1]
            this_pos = self.convert_int_pos_to_char(int_pos)
        return this_pos    