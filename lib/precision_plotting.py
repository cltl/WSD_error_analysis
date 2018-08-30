#import built-in modules
import os
import cPickle
from collections import defaultdict

#installed module or modules in this folder
from lxml import etree
import utils
import matplotlib.pyplot as plt
from precision_plotting_utils import plot
import pandas
import seaborn



filename2official_name = {
    '1.GAMBL-AW.all-words-test-predictions' : 'GAMBL',
    'PNNL.task-17.aw.txt' : 'PNNL',
    '128-627_Run-1000.txt' : 'CFILT-2',
    'keys-wn.2' : 'UMCC-DLSI',
    'SMUaw-' : 'SMUaw'
}

old2new = {'sval2' : 'se2-aw',
           'sval3' : 'se3-aw',
           'sval2007': 'se7-aw',
           'sval2010': 'se10-aw',
           'sval2013' : 'se13-aw'}


class PrecisionPlotting():
    '''
    
    @type  data: dict
    @ivar  data:
        feature_value ->
            'system' -> list of 0 and 1
                
    using the global variables defined in ../precision_errors.sh or .../
    (1) a graph (pdf file) is created with the average monosemous errors per competition
    '''
    def __init__(self):
        #dict mapping competition to .bin
        self.com_to_bin = utils.mapping_competition_to_bin()
        
        #dict mapping competition to xml file
        self.com_to_xml = utils.mapping_competition_to_xml()
        
        #set settings to class attributes
        self.settings_to_class_attributes()
        
        #set ivar data
        self.data = defaultdict(lambda: defaultdict(list))

        
        #loop
        self.loop()
        
        #plot
        plot(self.data,
             self.data.keys(),
             'Average precision per %s' % self.feature,
             '%s' % self.feature,
             'precision',
             os.environ['output_path_pdf'],
             12)

        #plot barplot
        list_of_lists = []
        headers = ['POS', 'Competition (System)', 'Recall']

        for feature_value in ['n', 'v', 'a', 'r']:
            for competition in ['sval2', 'sval3', 'sval2007', 'sval2010', 'sval2013']:
                for (the_competition, system_name), answers in self.data[feature_value].iteritems():

                    if the_competition == competition:

                        recall = float(sum(answers)) / len(answers)
                        official_name = filename2official_name[system_name]

                        one_row = [feature_value, old2new[competition] + ' (%s)' % official_name, recall]
                        list_of_lists.append(one_row)

        plt.figure(figsize=(15, 8))
        df = pandas.DataFrame(list_of_lists, columns=headers)
        ax = seaborn.barplot(x='POS', y='Recall', hue='Competition (System)', data=df)
        ax.legend(loc=2, title='Competition (Top System overall $F_{1}$)')
        ax.set_title('Recall per part of speech for each top ranked system')

        output_path = os.environ['barplot_path_pdf']
        plt.savefig(output_path)

        print 'barplot saved to', output_path




    def settings_to_class_attributes(self):
        '''
        this method set experiment settings to class attributes
        '''
        self.competitions = os.environ['competitions'].split("_")
        self.rankings     = os.environ['rankings']
        if self.rankings != "u":
            self.rankings = int(self.rankings)
        self.unranked     = os.environ['unranked']
        self.feature      = os.environ['feature']
        
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
                identifier    = token_el.get("token_id")
                feature_value = info[identifier][self.feature]
                
                #continue if pos == 'u'
                #if feature_value == "u":
                #    print competition, identifier, system_name, feature_value, 'not found'
                #    continue
                
                gold = [key.get("value")
                        for key in token_el.iterfind("gold_keys/key")]
                
                #loop over systems and write to file
                for system_el in token_el.iterfind('systems/system'):
                    
                    #check if system is ok in terms of exp settings
                    system_name = system_el.get("id")
                    system_rank = ""
                    
                    try:
                        system_rank = rankings[system_name]
                    except KeyError:
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
                        self.data[feature_value][(competition, system_name)].append(answer)


                        
                        
if __name__ == "__main__":
    PrecisionPlotting()