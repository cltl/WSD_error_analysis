import argparse
import glob
import os
from collections import defaultdict


#parse user input
parser = argparse.ArgumentParser(description='Convert output wsd error analysis to latex tables')

parser.add_argument('-i', dest='input_folder',     help='folder or file with output wsd error analysis',  required=True)
parser.add_argument('-t', dest='type_of_analysis', help='gs_stats |',                             required=True)
args = parser.parse_args()
competitions = ['sval2','sval3','sval2007','sval2010','sval2013']
old2new = {'sval2' : 'se2-aw',
           'sval3' : 'se3-aw',
           'sval2007': 'se7-aw',
           'sval2010': 'se10-aw',
           'sval2013' : 'se13-aw'}

new2wn_version = {'se2-aw' : '1.7',
                  'se3-aw' : '1.7.1',
                  'se7-aw' : '2.1',
                  'se10-aw' : '3.0',
                  'se13-aw' : '3.0',
                  'se15-aw' : '3.0'
                  }



if args.type_of_analysis == "gs_stats":
    
    output_path = os.path.join(args.input_folder,
                               'gs_stats_table.tex')
    features    = ['POS', '# docs','# instances']
    data = defaultdict(dict)
    
    for competition_output in glob.glob("{input_folder}/*.txt".format(input_folder=args.input_folder)):
        with open(competition_output) as infile:
            
            #competition
            com = os.path.basename(competition_output).strip(".txt")
            
            #info about competition
            for line in infile:
                key,value = line.strip().split("\t")
                data[com][key] = value
                
    with open(output_path,'w') as outfile:
        
        string = "%% created with function %s in clin.2015.sh\n\n" % args.type_of_analysis
        string += '''\\begin{table}[!h]\n\\label{tab:gs_stats}\n\\begin{tabular}{ c || c c c c c}\n'''
        string += "&".join(["\\textbf{%s} " % header.replace("_","\\_") for header in ['task']+['WordNet version'] + features]) + "\\\\ \n"
        string += '\\hline \\hline\n'
        
        for competition in competitions:

            new_name = old2new[competition]
            wn_version = new2wn_version[new_name]

            
            info = data[competition]


            values = [new_name] + [wn_version] + [info[feature] for feature in features]


            string += " & ".join(values) + " \\\\ \n"

            if new_name == 'se2-aw':
                values = ['se2-aw-v2', '3.0', 'a n nr v', '3', '2282']
                string += " & ".join(values) + " \\\\ \n"

        #write end
        values = ['se15-aw', '3.0', 'a n r v', '4', '1119']
        string += " & ".join(values) + " \\\\ \n"
        string += "\\end{tabular}\n\\caption{TODO}\n\\end{table}\n"

        outfile.write(string)
    


if args.type_of_analysis == "logistic_regression":
    
    output_path = args.input_folder + ".tex"
    features    = ['Coefficients', 'Estimate', 'Std. Error','z value','Pr(>|z|)']
    
    with open(output_path,'w') as outfile:
        
        string = "%% created with function %s in clin.2015.sh\n\n" % args.type_of_analysis
        string += '''\\begin{table}\n\\begin{tabular}{ r || c c c c}\n'''
        string += "&".join(["\\textbf{%s} " % header.replace("_","\\_") for header in features]) + "\\\\ \n"
        string += '\\hline \\hline\n'
        
        coefficient_line = 0
        with open(args.input_folder) as infile:
            for counter, line in enumerate(infile):
                
                if line.startswith("(Dis"):
                    break
                
                elif line == "\n":
                    continue
                
                elif line.startswith("---"):
                    continue
                    
                elif line.startswith("Sign"):
                    line = '''\\multicolumn{5}{l}{Signif. codes:  0 ``$\\ast$$\\ast$$\\ast$'' 0.001 ``$\\ast$$\\ast$'' 0.01 ``$\\ast$'' 0.05 ``.'' 0.1 `` '' 1}\\\\\n'''
                    string += line
                    
                elif line.startswith("Coefficients"):
                    coefficient_line = counter
                
                elif all([coefficient_line,
                        counter >= (coefficient_line+2)]):
                    values = line.strip().split()
                    
                    if values[-1] in ['***','**','*','.',' ']:
                        ending = values[-1]
                        values = values[:-1]
                        values[-1] = values[-1] + " " + ending
                        
                        if values[-2] in ['<']:
                            
                            values.pop(-2)
                            values[-1] = '< '+values[-1]
                    
                    for counter,value in enumerate(values):
                        if counter in [1,2,3]:
                            try:
                                #value = str( round( float(value) ,3) )
                                value = '{:.3f}'.format(round(float(value), 3))
                                values[counter] = value
                            except:
                                continue
                        
                    values = [value.replace("_","\\_") for value in values]
                    string += " & ".join(values) + " \\\\ \n"
            
        #write end

        string += "\\end{tabular}\n\\caption{TODO}\n\\end{table}"
        
        outfile.write(string)
      
    