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



if args.type_of_analysis == "gs_stats":
    
    output_path = os.path.join(args.input_folder,
                               'gs_stats_table.tex')
    features    = ['pos','num_docs','num_tokens','num_types','type_token_ratio']
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
        string += "&".join(["\\textbf{%s} " % header.replace("_","\\_") for header in ['task']+features]) + "\\\\ \n"
        string += '\\hline \\hline\n'
        
        for competition in competitions:
            
            info = data[competition]
            values = [competition] + [info[feature] for feature in features]
            
            string += " & ".join(values) + " \\\\ \n"
            
        #write end
        string += "\\end{tabular}\n\\caption{TODO}\n\\end{table}\n"

        outfile.write(string)
    


if args.type_of_analysis == "logistic_regression":
    
    output_path = args.input_folder + ".tex"
    features    = ['Coefficients', 'Estimate', 'Std. Error','z value','Pr(>|z|)']
    
    with open(output_path,'w') as outfile:
        
        string = "%% created with function %s in clin.2015.sh\n\n" % args.type_of_analysis
        string += '''\\begin{table}\n\\label{tab:TODO}\n\\begin{tabular}{ r || c c c c}\n'''
        string += "&".join(["\\textbf{%s} " % header.replace("_","\\_") for header in features]) + "\\\\ \n"
        string += '\\hline \\hline\n'
        
        coefficient_line = 0
        with open(args.input_folder) as infile:
            for counter, line in enumerate(infile):

                if line.startswith("---"):
                    break
                
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
                    
                    values = [value.replace("_","\\_") for value in values]
                    string += " & ".join(values) + " \\\\ \n"
            
        #write end
        string += "\\end{tabular}\n\\caption{TODO}\n\\end{table}"
        
        outfile.write(string)
      
    