
# coding: utf-8

# In[1]:


# libraries
import pandas
import numpy as np
from collections import defaultdict
import utils
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import seaborn
from matplotlib.ticker import MaxNLocator


# In[2]:


path = 'Systems.xlsx'


# In[3]:


df = pandas.read_excel(path)


# In[4]:


headers = ['Year', 'Freq', 'Category']


# In[5]:


rows = []
year2categories = defaultdict(list)

for index, row in df.iterrows():
    cat = row['category']
    year = row['year']
    year2categories[year].append(utils.category2abbreviation[cat])

for year, categories in year2categories.items():
    
    for cat in set(categories):
        row = [year]
        row.append(categories.count(cat))
        row.append(cat)
    
        rows.append(row)

plot_df = pandas.DataFrame(rows, columns=headers)


# In[6]:


# multiple line plot
ax = plt.figure(figsize=(20,10))
ax.gca().yaxis.set_major_locator(MaxNLocator(integer=True))


seaborn.barplot(x='Year', y='Freq', data=plot_df, hue='Category')


# Custom X axis
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title('Number of publications per WSD category per year', fontsize=22)
plt.xlabel("Publication Year", fontsize=20)
plt.ylabel("# of publications", fontsize=20)
plt.legend(fontsize=20)




# Show graphic
plt.savefig('output/types_over_the_years.pdf')

