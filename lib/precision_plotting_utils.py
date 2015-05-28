from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt
from pylab import *

def plot(data,
         labels,
         title_graph,
         x_label,
         y_label,
         output_path,
         size_of_font):
    '''
    given a defaultdict mapping from string to list of floats
    a boxplot is created
    
    @type  data:  defaultdict
    @param data:  defaultdict mapping from pos -> system_name -> list of 0 and 1
    
    @type  labels: list
    @param labels: list of labels the feature can have in the order
    you want to have it plotted
    '''
    input_boxplot = []
    
    for label in labels:
        if label in data:
            output = []
            for system_name,system_output in data[label].iteritems():
                
                precision = 100 * sum(system_output)/len(system_output) 
                    
                output.append(precision)
            
            input_boxplot.append(output)
    
    #convert list of lists to np.array
    input_boxplot = map(np.asarray,input_boxplot)
    
    # multiple box plots on one figure
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    
    #set xTicks
    xTickMarks = labels
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, fontsize=size_of_font)
    
    #set title
    plt.title(title_graph)
    
    #set x and y axis labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    boxplot(input_boxplot)

    plt.savefig(output_path)
    plt.close()