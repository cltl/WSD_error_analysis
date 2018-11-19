#import built-in modules
import os
import cPickle
from collections import defaultdict

#installed module or modules in this folder
from lxml import etree
import utils
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

'''

IAA
(1) sval2 http://www.aclweb.org/anthology/S01-1005: NA
(2) sval3 http://www.aclweb.org/anthology/W/W04/W04-0811.pdf 72.5
(3) sval2007 http://www.aclweb.org/anthology/S/S07/S07-1016.pdf verbs 72 nouns 86
(4) sval2010 http://www.aclweb.org/anthology/S10-1013: one annotator: not available
(5) sval2013 not available
'''


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
        self.labels = ['sval2','sval3','sval2007','sval2010','sval2013']
        
        #loop and write
        self.loop()
        self.plot_it()

        
    def loop(self):
        '''
        this method loops over the competitions in the folder
        'sval_systems' and updates the class attributes
        '''

        answer_is_u = defaultdict(set)

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

                if any([gold == ['U'],
                        identifier == 'd001.s044.t009']):
                    answer_is_u[competition].add(identifier)
                    continue
                
                #check if gold is mfs
                mfs = info[identifier]['MFS'] == "Yes_MFS"
                
                #loop over systems and write to file
                for system_el in token_el.iterfind('systems/system'):
                    
                    system_keys = [answer_el.get('value')
                                   for answer_el in system_el.iterfind('answer')]


                    system_name = system_el.get("id")
                    try:
                        system_rank = rankings[system_name]
                    except KeyError:
                        pass

                    allowed = False
                    if all([isinstance(system_rank, int),
                            system_rank <= 1]):
                        allowed = True
                    
                    # check if answer was correct
                    answer = 0
                    if any([system_key in gold
                            for system_key in system_keys]):
                        answer = 1


                    if allowed:
                        assert system_name in filename2official_name

                        if mfs:
                            acc_mfs.append(answer)

                        else:
                            acc_notmfs.append(answer)


            #if competition != "sval2010":
            self.mfs[competition]    = 100 * sum(acc_mfs)/float(len(acc_mfs))
            self.notmfs[competition] = 100 * sum(acc_notmfs)/float(len(acc_notmfs))

        for competition, ids in answer_is_u.items():
            print('# of U answers', competition, len(ids))
            
    def plot_it(self):
        '''
        given self.mfs and self.notmfs and self.labels a plot is created
        '''
        matplotlib.rc('font', family='sans-serif') 
        matplotlib.rc('font', serif='times') 
        matplotlib.rc('text', usetex='false') 
        matplotlib.rcParams.update({'font.size': 20})
        
        fig = plt.figure(figsize=(16, 10))
        ax = fig.add_subplot(111)
        
        ## the data
        N = 5
        menMeans   = [self.mfs[comp]    for comp in self.labels]
        menStd     = [0, 0, 0, 0, 0]
        womenMeans = [self.notmfs[comp] for comp in self.labels]
        womenStd   = [0, 0, 0, 0, 0]
        
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
        ax.set_xlabel('Senseval/SemEval competition')
        ax.set_ylabel('Recall')
        ax.set_title('Recall on MFS vs LFS of top ranked systems')
        xTickMarks = [old2new[label] for label in self.labels]
        ax.set_xticks(ind+width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=60, fontsize=20)
        
        ## add a legend
        ax.legend( (rects1[0], rects2[0]), ('MFS', 'LFS') )
        
        #save

        plt.savefig(os.environ['output_pdf'], bbox_inches='tight')
        
if __name__ == "__main__":
    MFS_or_not_MFS()    