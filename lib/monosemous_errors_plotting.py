import os
import matplotlib.pyplot as plt


#from matplotlib import rc 
#rc('font', family='serif', serif='Vera Sans Roman') 


output_path = os.path.join(os.environ['cwd'],
                           'output',
                           'monosemous_errors',
                           'monosemous_errors.pdf')


old2new = {'sval2' : 'se2-aw',
           'sval3' : 'se3-aw',
           'sval2007': 'se7-aw',
           'sval2010': 'se10-aw',
           'sval2013' : 'se13-aw'}

x_average = []
y_average = []
with open(os.environ['average']) as infile:
        for line in infile:
            competition, error_rate = line.strip().split("\t")

            new_label = old2new[competition]
            x_average.append(new_label)
            y_average.append(float(error_rate))

x_top = []
y_top = []
with open(os.environ['top']) as infile:
        for line in infile:
            competition,error_rate = line.strip().split("\t")
            x_top.append(competition)
            y_top.append(float(error_rate))

fig    = plt.figure()
ax     = fig.add_subplot(111)
x_axis = range(len(x_average))


plt.plot(x_axis, y_average,     label="average all systems")
plt.plot(x_axis,     y_top,     label="top system")
        
plt.title("error rate monosemous instances per competition")
plt.xlabel("semeval competition")
plt.ylabel("monosemous error rate (%)")
plt.xticks(range(len(x_average)), x_average, size='small')
plt.xticks(rotation=45)
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax.legend(loc=1
          #bbox_to_anchor=(0, 0.25)
          )

plt.savefig(output_path,dpi=100)
plt.close()