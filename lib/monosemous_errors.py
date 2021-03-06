#import built-in modules
import os
import cPickle
from collections import defaultdict

#installed module or modules in this folder
from lxml import etree
import utils
import matplotlib.pyplot as plt

class MonosemousErrors():
    '''
    using the global variables defined in ../monosemous_errors.sh
    (1) a txt file is created with the average monosemous errors per competition
    (2) a graph (pdf file) is created with the average monosemous errors per competition
    '''
    def __init__(self):
        #dict mapping competition to .bin
        self.com_to_bin = utils.mapping_competition_to_bin()
        
        #dict mapping competition to xml file
        self.com_to_xml = utils.mapping_competition_to_xml()
        
        #set settings to class attributes
        self.settings_to_class_attributes()
        
        #loop
        self.loop()
        
        #plot
        outfile = open(os.environ['output_path_txt'],"w") 
        for counter,competition in enumerate(self.competitions):
            if competition in self.results:
                mistakes   = float(self.results[competition].count(0))
                error_rate = 100 * (  mistakes/len(self.results[competition])  )
                outfile.write("%s\t%s\n" % (competition,error_rate))
        outfile.close()  
        
    def settings_to_class_attributes(self):
        '''
        this method set experiment settings to class attributes
        '''
        self.competitions = os.environ['competitions'].split("_")
        self.rankings     = os.environ['rankings']
        if self.rankings != "u":
            self.rankings = int(self.rankings)
        self.unranked     = os.environ['unranked']
        
    def loop(self):
        '''
        this method loops over the competitions in the folder
        'sval_systems' and create the output_path txt and pdf
        '''
        self.results = defaultdict(list)

        #loop
        for competition,xml_file in self.com_to_xml.iteritems():

            if competition not in self.competitions:
                continue
            
            bin_file     = self.com_to_bin[competition]
            com,info     = cPickle.load(open(bin_file))
            rankings     = utils.open_rankings_file(competition)
             
            doc      = etree.parse(xml_file)
            
            #loop over tokens and create list with values
            for token_el in doc.iterfind("token"):
                
                #obtain gold keys
                identifier = token_el.get("token_id")
                gold = [key.get("value")
                        for key in token_el.iterfind("gold_keys/key")]
                
                #check if gold lemma is monosemous
                if info[identifier]['num_senses'] != 1:
                    continue

                #loop over systems and write to file
                for system_el in token_el.iterfind('systems/system'):
                    
                    #check if system is ok in terms of exp settings
                    system_name = system_el.get("id")
                    system_rank = ""
                    try:
                        system_rank = rankings[system_name]
                    except KeyError:
                        #print system_name,'not found'
                        pass
                    
                    allowed = False
                    if all([system_rank == "u",
                            self.unranked == "yes"]):
                        allowed = True
                    if all([isinstance(system_rank,int),
                            system_rank <= self.rankings]):
                        allowed = True
                        
                    system_keys = [answer_el.get('value')
                                   for answer_el in system_el.iterfind('answer')]
                    
                    #check if answer was correct
                    answer = 0
                    if any([system_key in gold 
                           for system_key in system_keys]):
                        answer = 1
                    
                    #write to file
                    if allowed:
                        self.results[competition].append(answer)
        
                    
if __name__ == "__main__":
    MonosemousErrors()