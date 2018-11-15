from collections import defaultdict
from nltk.corpus import wordnet as wn

def get_lemma_pos_of_sensekey(sense_key):
    """
    lemma and pos are determined for a wordnet sense key

    >>> get_lemma_pos_of_sensekey('life%1:09:00::')
    ('life', 'n')

    :param str sense_key: wordnet sense key

    :rtype: tuple
    :return: (lemma, n | v | r | a | u)
    """
    if '%' not in sense_key:
        return '', 'u'

    lemma, information = sense_key.split('%')
    int_pos = information[0]

    if int_pos == '1':
        this_pos = 'n'
    elif int_pos == '2':
        this_pos = 'v'
    elif int_pos in {'3', '5'}:
        this_pos = 'a'
    elif int_pos == '4':
        this_pos = 'r'
    else:
        this_pos = 'u'

    return lemma, this_pos

def get_sensekey2rank(index_sense_path):
    sensekey2rank = dict()
    with open(index_sense_path) as infile:
        for line in infile: 
            fields = line.strip().split()
            sensekey, offset, rank, freq = fields
            
            lemma, pos = get_lemma_pos_of_sensekey(sensekey)
            
            polysemy = len(wn.synsets(lemma, pos))

            sensekey2rank[sensekey] = (int(rank), polysemy)
    
    return sensekey2rank

def get_sensekey_freq(annotations_path, sensekey2rank):
    rank2sensekey2freq = dict()
    total_sensekey_annotations = 0
    total_polysemous_annotations = 0

    with open(annotations_path) as infile:
        for line in infile:
            id_, *sensekeys = line.strip().split()
            for sensekey in sensekeys:
                rank, polysemy = sensekey2rank[sensekey]

                total_sensekey_annotations += 1

                if polysemy <= 1:
                    continue
                   
                total_polysemous_annotations += 1
                


                if rank not in rank2sensekey2freq:
                    rank2sensekey2freq[rank] = defaultdict(int)

                rank2sensekey2freq[rank][sensekey] += 1
    
    return rank2sensekey2freq, total_sensekey_annotations, total_polysemous_annotations

def get_rank2info(rank2sensekey2freq):
    rank2info = dict()
    for rank, sensekey2freq in sorted(rank2sensekey2freq.items()):

        number_of_annotations = sum(sensekey2freq.values())
        number_of_sensekeys = len(sensekey2freq)
        avg = number_of_annotations / number_of_sensekeys

        rank2info[rank] = (number_of_sensekeys, avg, number_of_annotations)
    
    return rank2info