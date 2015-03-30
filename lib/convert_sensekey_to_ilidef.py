from wordnet_reader import wordnet_reader
import argparse
import glob

from lxml import etree

def mapping_sensekey_ilidef(index_file):
    '''
    given a wordnet index_file
    
    @type  index_file: str
    @param index_file: path to wordnet index file containing lines:
    100%5:00:00:cardinal:00 02196107 1 33
    
    rtype: dict
    @return: mapping from sensekey to ilidef
    '''
    mapping = {}
    
    with open(index_file) as infile:
        for line in infile:
            sense_key,synset_offset, sense_number, tag_cnt = line.strip().split()
            
            pos_int = sense_key.split("%")[1][0]
            pos = wordnet_reader("").convert_int_pos_to_char(pos_int)
            
            ilidef = "ili-30-{offset}-{pos}".format(offset=synset_offset,
                                                    pos=pos)
            
            mapping[sense_key] = ilidef
    
    return mapping


if __name__ == "__main__":

    #parse user input
    parser = argparse.ArgumentParser(description='Adds ilidef elements on top off sense_keys in wsd_corpora')
    
    parser.add_argument('-i', dest='input_folder', help='full path to folder in which naf files are stored', required=True)
    parser.add_argument('-s', dest='index_file',   help='full path to wordnet index file',                   required=True)
    
    #convert command line arguments into dict a
    #and make every argument a local variable
    args = parser.parse_args().__dict__    
    for key,value in args.iteritems():
        locals()[key] = value
    
    #create mapping 
    mapping = mapping_sensekey_ilidef(index_file)
    
    for naf_file in glob.glob("{input_folder}/*".format(input_folder=input_folder)):
        
        #parse document using lxml.etree.parse
        doc = etree.parse(naf_file,etree.XMLParser(remove_blank_text=True))
                          
        #add externalRef el with mapping sensekey to ilidef
        path_to_sense_keys = "terms/term/externalReferences/externalRef[@reftype='sense']"
        
        #loop over externalRef with reftype='sense'
        for ext_refs_el in doc.iterfind(path_to_sense_keys):

            #get parent lxml element
            parent    = ext_refs_el.getparent()
            
            #get sense_key and mapping            
            sense_key = ext_refs_el.get("reference")
            ilidef    = mapping[sense_key]
            
            #crete new element
            attributes = ext_refs_el.attrib
            attributes['reftype']   = 'ilidef'
            attributes['reference'] = ilidef
            
            #insert element in file
            new_ext_ref_el = parent.makeelement('externalRef',
                                                attrib=attributes)
            parent.insert(0,new_ext_ref_el)
            
            #write to file 
            with open(naf_file+".test.naf","w") as outfile:
                doc.write(outfile,
                          pretty_print=True,
                          xml_declaration=True,
                          encoding='utf-8')
