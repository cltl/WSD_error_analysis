#import built-in modules
import os
import glob
import re
import ast

#installed modules
import matplotlib.pyplot as plt

def mapping_competition_to_bin():
    '''
    this function creates a mapping between a competition
    and the path to the cPickle object containing information about
    this competition
    '''
    #path to matrixes
    matrixes = os.path.join(os.environ['cwd'],
                            "data",
                            "matrices")
    
    #set class attribute
    com_to_bin = {}
    
    #loop
    for path_d in glob.glob("{matrixes}/*.bin".format(matrixes=matrixes)):
        competition = re.findall("{matrixes}/(.*)_matrix.bin".format(matrixes=matrixes),
                         path_d)[0]
        com_to_bin[competition] = path_d
    
    return com_to_bin


def mapping_competition_to_xml():
    '''
    this method creates a mapping between a competition
    and the path to the xml file containing information
    about the submissions to this competition
    '''
    #path to sval_systems
    sval_systems = os.path.join(os.environ['cwd'],
                                'data',
                                'sval_systems')
    
    #set class attribute
    com_to_xml = {}
    
    #loop
    for path in glob.glob("{sval_systems}/se*".format(sval_systems=sval_systems)):
        basename    = os.path.basename(path)
        competition = basename.split("_")[0]
        for to_replace,replacement in [('senseval','sval'),
                                       ('semeval', 'sval')]:
            competition = competition.replace(to_replace,replacement)
        xml         = glob.glob("{path}/*.xml".format(path=path))[0]
        com_to_xml[competition] = xml
    
    return com_to_xml

def obtain_identifier(identifier,
                      context_level,
                      competition,
                      d):
    '''
    given the identifier,context_level,competition an unique identifier 
    is returned
    
    @type  identifier: str
    @param identifier: identifier of token instance according to .bin
    
    @type  context_level: str
    @param context_level: 'all' 'document' 'sentence' 'word'
    
    @type  competition: str
    @param competition: sval2 sval3 sval2007 sval2010 sval2013
    
    @type  d: dict
    @param d: dict containing information about one instance of a
    senseval/semeval competition
    
    @rtype: str
    @return: unique identifier 
    '''
    uri = "all"
    
    if context_level == 'word':
        uri = identifier
    
    elif context_level == "sentence":
        uri = d['sentence_identifier']
    
    elif context_level == "document":
        uri = d['sentence_identifier'].split(".")[0]

    return competition+"+++"+uri


def obtain_highest_score(d):
    '''
    given a dict
    
    @type  d: dict
    @param d:   'lemma':
                'monosemous'   : bool
                'pos'          : n | v | r | a | u
                'keys'         : list
                'num_instances': int
                'instances'    : list of tuples (iden, [gold keys], sentence)
                
    @rtype: int
    @return: max number of instances correct if one sense chosen.
    '''
    max_correct = 0
    
    #obtain set gold keys
    set_gold_keys = []
    for uri,valid_skeys,sentence in d['instances']:
        for key in valid_skeys:
            set_gold_keys.append(key)
            
    for gold_key in set_gold_keys:
        num_correct = [gold_key in valid_skeys
                       for uri,valid_skeys,sentence in d['instances']
                        ].count(True)
        if num_correct > max_correct:
            max_correct = num_correct
    
    return max_correct



def plot_it(data, context_levels,competitions, allowed_pos):
    '''
    
    @type  context_levels: list
    @param context_levels: list of context levels
    
    @type  data: dict
    @param data: 'context level':
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
                        'perc_hapax_instances'    float
    '''
    output_path = os.environ['output_path']
    
    #x values
    x_values = context_levels
    
    #y values
    lists_of_y_values = [(categorie,[data[context_level][categorie] for context_level in context_levels])
                         for categorie in ['perc_correct','perc_monosemous','perc_hapax_instances']
                         ]
    
    #plot it
    fig    = plt.figure()
    ax     = fig.add_subplot(111)
    x_axis = range(len(x_values))
    
    for label,list_of_y_values in lists_of_y_values:
        plt.plot(x_axis,list_of_y_values,label=label)
    
    #try to fit xlabel in plot
    plt.gcf().subplots_adjust(bottom=0.20)
    
    plt.title("Predominant sense %s %s" % (competitions,allowed_pos))
    plt.xlabel("context level")
    plt.ylabel("max performance per context level (if you know pos)")
    plt.xticks(range(len(x_values)), x_values, size='small')
    plt.xticks(rotation=90)
    ax.legend(loc='lower right')
    
    #plt.show()
    plt.savefig(output_path,dpi=100)
    plt.close()

def one_sense_used(lijst):
    senses = []
    for uri,list_senses,sentence in lijst:
        for sense in list_senses:
            senses.append(sense)
    
    num_instances = len(lijst)
    
    max_count = 0
    for sense in set(senses):
        count = senses.count(sense)
        if count > max_count:
            max_count = count
    
    not_predominant = num_instances-max_count
    return (max_count < num_instances,not_predominant)


def open_rankings_file(competition):
    '''
    given a competition, the rankings dict is returned
    
    @type  competition: str
    @param competition: sval2 | sval3 | sval2007 | sval2010 | sval2013
    
    @rtype: dict
    @return: rankings dict mapping system submission to rank in competition
    '''
    path = os.path.join(os.environ['cwd'],
                        'data',
                        'rankings',
                        competition)
    
    with open(path) as infile:
        return ast.literal_eval(infile.read())
