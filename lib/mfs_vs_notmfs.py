#import built-in modules
import os
import cPickle

#installed module or modules in this folder
from lxml import etree
import utils
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class MFS_or_not_MFS():
    '''
    using the global variables defined in ../plots_mfs_vs_not_mfs.sh
    (1) a plot (.pdf) is created
    (2) stats about the competitions are written to file
    '''
    def __init__(self):
        #dict mapping competition to .bin
        self.com_to_bin = utils.mapping_competition_to_bin()
        
        #dict mapping competition to xml file
        self.com_to_xml = utils.mapping_competition_to_xml()
        
        #class attributes
        self.mfs    = {}
        self.notmfs = {}
        self.labels = ['sval2','sval3','sval2007','sval2013']
        
        #loop and write
        self.loop()
        self.plot_it()

        
    def loop(self):
        '''
        this method loops over the competitions in the folder
        'sval_systems' and updates the class attributes
        '''
      
        #loop
        for competition,xml_file in self.com_to_xml.iteritems():
                
            #set lists
            acc_mfs                = []
            acc_notmfs             = []
            
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
                
                #check if gold is mfs
                mfs = info[identifier]['MFS'] == "Yes_MFS"
                
                #loop over systems and write to file
                for system_el in token_el.iterfind('systems/system'):
                    
                    system_keys = [answer_el.get('value')
                                   for answer_el in system_el.iterfind('answer')]
                    
                    #check if answer was correct
                    answer = 0
                    
                    if any([system_key in gold 
                            for system_key in system_keys]):
                        answer = 1

                    if mfs:
                        acc_mfs.append(answer)
                        
                    else:
                        acc_notmfs.append(answer)
                

            if competition != "sval2010":
                self.mfs[competition]    = 100 * sum(acc_mfs)/float(len(acc_mfs))
                self.notmfs[competition] = 100 * sum(acc_notmfs)/float(len(acc_notmfs))
            
    def plot_it(self):
        '''
        given self.mfs and self.notmfs and self.labels a plot is created
        '''
        matplotlib.rc('font', family='sans-serif') 
        matplotlib.rc('font', serif='times') 
        matplotlib.rc('text', usetex='false') 
        matplotlib.rcParams.update({'font.size': 15})
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        ## the data
        N = 4
        menMeans   = [self.mfs[comp]    for comp in self.labels]
        menStd     = [0, 0, 0, 0]
        womenMeans = [self.notmfs[comp] for comp in self.labels]
        womenStd   = [0, 0, 0, 0]
        
        ## necessary variables
        ind = np.arange(N)                # the x locations for the groups
        width = 0.35                      # the width of the bars
        
        ## the bars
        rects1 = ax.bar(ind, menMeans, width,
                        color='black')
        
        rects2 = ax.bar(ind+width, womenMeans, width,
                            color='red')
        
        # axes and labels
        ax.set_xlim(-width,len(ind)+width)
        ax.set_ylim(0,100)
        ax.set_ylabel('Accuracy')
        ax.set_title('Accuracy when sense is MFS versus when it is not')
        xTickMarks = ['sval2','sval3','sval2007','sval2013']
        ax.set_xticks(ind+width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=45, fontsize=10)
        
        ## add a legend
        ax.legend( (rects1[0], rects2[0]), ('MFS', 'NotMFS') )
        
        #save
        plt.savefig(os.environ['output_pdf'])    
        
if __name__ == "__main__":
    MFS_or_not_MFS()    