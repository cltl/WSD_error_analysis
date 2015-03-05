#import built-in modules
import os
import cPickle

#installed module or modules in this folder
from lxml import etree
import utils

class Semeval2R():
    '''
    using the global variables defined in ../logistic_regression.sh
    (1) a csv file is generated based on those settings.
    (2) an .R script is generated to run logistic regression
    '''
    def __init__(self):
        #dict mapping competition to .bin
        self.com_to_bin = utils.mapping_competition_to_bin()
        
        #dict mapping competition to xml file
        self.com_to_xml = utils.mapping_competition_to_xml()
        
        #set settings to class attributes
        self.settings_to_class_attributes()
        
        #loop and write
        self.loop()
        
    def settings_to_class_attributes(self):
        '''
        this method set experiment settings to class attributes
        '''
        self.competitions = os.environ['competitions'].split("_")
        self.allowed_pos  = os.environ['allowed_pos'].split('_')
        self.features     = os.environ['features'].split("---")
        self.rankings     = os.environ['rankings']
        if self.rankings != "u":
            self.rankings = int(self.rankings)
        self.unranked     = os.environ['unranked']
        
    def loop(self):
        '''
        this method loops over the competitions in the folder
        'sval_systems' and create the output_path
        '''
        #create R script
        with open(os.environ["model_Rscript"]) as infile:
            raw = infile.read()
        
        #change raw with experiment settings
        raw       = raw.replace("CSV_INPUT",os.environ['output_path'])
        variables = " + ".join(self.features)
        raw       = raw.replace("VARIABLES",variables)
        with open(os.environ['Rscript'],"w") as outfile:
            outfile.write(raw)
             
        #create csv file
        with open(os.environ['output_path'],"w") as outfile:
            
            #write headers to file
            headers = ['correct'] + self.features
            outfile.write(",".join(headers)+"\n")
            
            #loop
            for competition,xml_file in self.com_to_xml.iteritems():
                
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
                    
                    #set properties
                    output = [info[identifier][feature]
                              for feature in self.features]
                    
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
                            to_file = [answer] + output
                            to_file = [str(item) for item in to_file]
                            outfile.write(",".join(to_file)+"\n")
                    
if __name__ == "__main__":
    Semeval2R()