import os
import sys
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class sval_systems_reader:
    def __init__(self, path_to_folder):
        self.path_to_folder = path_to_folder
        
    def get_path_to_file(self, which_corpus):
        path_to_xml = ''
        if which_corpus.lower() in ['sval2', 'senseval2']:
            path_to_xml = os.path.join(self.path_to_folder,'senseval2','senseval2.xml')
        elif which_corpus.lower() in ['sval3', 'senseval3']:
            path_to_xml = os.path.join(self.path_to_folder,'senseval3','senseval3.xml')
        elif which_corpus.lower() in ['semeval2007', 'sval2007']:
            path_to_xml = os.path.join(self.path_to_folder,'semeval2007_task17_allwords','semeval2007_task17_allwords.xml')
        elif which_corpus.lower() in ['semeval2010', 'sval2010']:
            path_to_xml = os.path.join(self.path_to_folder,'semeval2010_task17','semeval2010_task17_en.xml')
        elif which_corpus.lower() in ['semeval2013', 'sval2013']:
            path_to_xml = os.path.join(self.path_to_folder,'semeval2013_task12','semeval2013_task12_wn.xml')
        else:
            path_to_xml = None
        return path_to_xml
            
            
            
    def get_gold_id_and_labels(self,which_corpus):
        path_to_xml = self.get_path_to_file(which_corpus)
        if path_to_xml is None:
            print>>sys.stderr,'Error. Corpus identifier %s not valid. Use: sval2 sval3 semeval2007 semeval2010 or semeval2013' % which_corpus
            sys.exit(-1)
        my_tree = ET.parse(path_to_xml)
        
        for token in my_tree.findall('token'):
            this_id = token.get('token_id')
            labels = [key.get('value') for key in token.findall('gold_keys/key')]
            yield this_id, labels
            
                    
if __name__ == '__main__':
    my_reader = sval_systems_reader('/home/izquierdo/ulm1/WSD_logistic_regression/data/sval_systems')
    for this_id, labels in my_reader.get_gold_id_and_labels('sval3'):
        print this_id, labels           