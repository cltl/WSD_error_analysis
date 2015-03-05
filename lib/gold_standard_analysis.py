#import built-in modules
import os
import cPickle
from collections import defaultdict
import operator

#import module from this folder
import utils

class GS_analysis():
    '''
    goal of this class is to use the global variables defined in 
    ../plots_gold_standards.sh and plot information about the gold standards
    
    @todo: filtering on pos
    @todo: plotting
    @todo: write statistics
    
    structure of dict
    'context level':
        'lemmas'
            'lemma':
                'monosemous'   : bool
                'pos'          : n | v | r | a | u
                'keys'         : list
                'num_instances': int
                'instances'    : list of tuples (iden, [gold keys], sentence)

        'num_correct':            int
        'num_instances':          int
        'num_monosemous           int'
        'num_no_hapax_instances'  int
        'perc_correct'            float
        'perc_monosemous'         float
        'perc_no_hapax_instances' float
        
    '''
    def __init__(self):
        #set class attribute data
        self.context_levels = ['all','document','sentence','word']
        self.data = {context_level:{}
                     for context_level in self.context_levels}
        for context_level in self.context_levels:
            self.data[context_level]['lemmas'] = {}

        #get dict competition to .bin and set class attributes of exp settings
        self.competitions = os.environ['competitions'].split("_")
        self.allowed_pos  = os.environ['allowed_pos'].split('_')
        self.com_to_bin = {competition:path 
                           for competition,path in utils.mapping_competition_to_bin().iteritems()
                           if competition in self.competitions}
        
        #update ivar data with .bin
        self.loop_bins()
        
        #plot + write information to file
        utils.plot_it(self.data,
                      self.context_levels, 
                      self.competitions, 
                      self.allowed_pos)
        
        #write stats to file
        for context_level in self.context_levels:
            output_file = os.path.join(os.environ['output_folder'],context_level+".csv")
            stat_file   = open(output_file+"stats.csv","w")
            stats       = defaultdict(int)
            with open(output_file,"w") as outfile:
                headers = "\t".join(['lemma','pos','num_instances','instances'])
                outfile.write(headers+"\n")
                for uri,info in self.data[context_level]['lemmas'].iteritems():
                    for lemma,d in info.iteritems():
                        not_one_sense,how_much = utils.one_sense_used(d['instances'])
                        if all([d['num_instances'] >= 2,
                                not_one_sense
                                ]):
                            stats[lemma] += how_much
                            output_line = [lemma,d['pos'],d['num_instances']] + d['instances']
                            output_line = map(str,output_line)
                            outfile.write("\t".join(output_line)+"\n")
            
            stat_file.write("lemma\toccurences\n")
            for lemma,instances in sorted(stats.iteritems(), 
                                          key=operator.itemgetter(1),
                                          reverse=True):
                stat_file.write("%s\t%s\n" % (lemma,instances))
            stat_file.close()
            
    def process_one_entry(self,uri,context_level,d):
        '''
        given uri, context_level and d, ivar data is updated with structure
        defined in docstring of this class
        
        @type  uri: str
        @param uri: identifier of token instance according to .bin
        
        @type  context_level: str
        @param context_level: 'all' 'document' 'sentence' 'word'
        
        @type  d: dict
        @param d: dict containing information about one instance of a
        senseval/semeval competition
        '''
        #get lemma
        lemma = d['lemma']
        pos   = d['pos']
        
        if pos not in self.allowed_pos:
            return 
        
        #create empty dic if uri not in self.data
        if uri not in self.data[context_level]['lemmas']:
            self.data[context_level]['lemmas'][uri] = {}
            
        #check lemma in  ivar data and update lemma entry
        if lemma in self.data[context_level]['lemmas'][uri]:
                
            info  = self.data[context_level]['lemmas'][uri][lemma]
            info['num_instances'] += 1
            info['instances'].append((uri,d['valid_skeys'],d['sentence']))
        
        #else, create entry for lemma
        else:
            info = {'monosemous'   : d['num_senses'] == 1,
                    'pos'          : d['pos'],
                    'keys'         : d['list_senses'],
                    'num_instances': 1,
                    'instances'    : [(uri,d['valid_skeys'],d['sentence'])]
                   }
        
            #update dict
            self.data[context_level]['lemmas'][uri][lemma] = info
        
    def loop_bins(self):
        '''
        this method loops the competitions in ivar com_to_bin
        and updates ivar data with the information explained in the docstring
        of this class
        '''
        #loop through competitions
        for competition,path in self.com_to_bin.iteritems():
            
            #load bin
            com,info = cPickle.load(open(path))
            
            #loop context_level
            for context_level in self.context_levels:
                
                #loop bin
                for identifier,d in info.iteritems():
                    
                    #obtain uri based on settings
                    uri = utils.obtain_identifier(identifier, context_level, competition, d)
                    
                    #process one instance of senseval/semeval
                    self.process_one_entry(uri,context_level,d)

        #create general counts
        for context_level in self.context_levels:
            general_d = self.data[context_level]
            
            #create list of tuples to loog through
            relevant = []
            for uri,info in general_d['lemmas'].iteritems():
                for lemma,d in info.iteritems():
                    relevant.append((lemma,d))
                    
            #'num_correct':            int
            num_correct    = sum([utils.obtain_highest_score(value)
                                  for key,value in relevant])
            
            #'num_instances':          int
            num_instances  =  sum([value['num_instances']
                                   for key,value in relevant])
                               
            #'num_monosemous           int'
            num_monosemous =  sum([value['num_instances']
                                   for key,value in relevant
                                   if value['monosemous']])
            

            #'num_no_hapax_instances'  int
            num_hapax_instances = sum([value['num_instances']
                                          for key,value in relevant
                                          if value['num_instances'] == 1])
            
            #'perc_correct'            float
            perc_correct    = float(num_correct)/float(num_instances)
            
            #'perc_monosemous'         float
            perc_monosemous = float(num_monosemous)/float(num_instances)

            #'perc_hapax_instances' float
            perc_hapax_instances = float(num_hapax_instances)/float(num_instances)
            
            general_info = {'num_correct':             num_correct,
                            'num_instances':           num_instances,
                            'num_monosemous':          num_monosemous,
                            'num_hapax_instances':     num_hapax_instances,
                            'perc_correct':            perc_correct,
                            'perc_monosemous':         perc_monosemous,
                            'perc_hapax_instances': perc_hapax_instances}
            
            self.data[context_level].update(general_info)
            
if __name__ == "__main__":
    GS_analysis()