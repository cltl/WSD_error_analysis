"""
Usage:
  plot_wsd_f1_trends.py --input_path=<wsd_state_of_the_art> --competitions=<competitions> --output_folder=<output_folder>

Options:
  -h --help     Show this screen.
  --input_path=<wsd_state_of_the_art> path to excel with overview wsd state of the art results
  --competitions=<competitions> separated by underscore the competitions you want to focus on (se2-aw, se2-aw-v2, se13-aw, se13-aw-v2)
  --output_folder=<output_folder> folder where plot will be stored
"""
from docopt import docopt
import os
import utils
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

import matplotlib.font_manager

from matplotlib.patches import Patch
from matplotlib.lines import Line2D

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.sans-serif'] = ['Lucida Grande']

# load arguments
arguments = docopt(__doc__)
print()
print('PROVIDED ARGUMENTS')
print(arguments)
print()

assert arguments['--input_path'].endswith('xlsx')

competitions = set(arguments['--competitions'].split('_'))

accepted_competitions = {'se2-aw', 'se2-aw-v2',
                         'se13-aw', 'se13-aw-v2'}
for competition in competitions:
    assert competition in accepted_competitions

if not os.path.exists(arguments['--output_folder']):
    os.mkdir(arguments['--output_folder'])

output_path = os.path.join(arguments['--output_folder'], arguments['--competitions'] + '.pdf')
data_path = os.path.join(arguments['--output_folder'], arguments['--competitions'] + '.p')
main_df = pandas.read_excel(arguments['--input_path'])
the_competition = min(competitions)


# load + validate data
systems, comp_df = utils.extract_relevant_rows(df=main_df,
                                               sense_repository='WordNet',
                                               the_competitions=competitions)

# create plot data
plot_df = utils.load_relevant_data_from_rows(comp_df, the_competition)
plot_df = plot_df.sort_values(by=['Year'], ascending=True)

# create plot
#ax = sns.lineplot(x='System', y='F1',
#                  #marker='o',
#                  data=plot_df)
#plt.tight_layout()
#plt.ylim(0.5, None)
#ax = sns.catplot(x='Year', y='F1', data=plot_df, hue='System')

plt.figure(figsize=(22, 10))
ax = sns.barplot(x='System', y='F1', data=plot_df,
                 color='white')

ax.set_xlabel('System', fontsize=30)
ax.set_ylabel('$F_1$', fontsize=30)
plt.ylim(0.5, None)
#plt.tight_layout()
plt.subplots_adjust(bottom=0.33)
ax.set_xticklabels(plot_df['System'], rotation=90)

plt.xticks(size=22)
plt.yticks(size=22)
rects = ax.patches

# Make some labels.
labels = []
ordered_systems = []
for index, row in plot_df.iterrows():

    if row['In_competition'] == 'yes':
        label = f'{row["Year"]} (IN)'
    else:
        label = f'{row["Year"]}'

    ordered_systems.append(row['System'])
    labels.append(label)

# best performing systems
maximum = max(plot_df['F1'])

print(plot_df)

top_indices = set()
for position, (index, row) in enumerate(plot_df.iterrows()):

    if row['F1'] == maximum:
        top_indices.add(position)

        print(maximum, row['System'])


system2color = utils.system_label2color('Systems.xlsx')

for index, (rect, label, system) in enumerate(zip(rects, labels, ordered_systems)):

    if index in top_indices:
        rect.set_hatch('*')

    size_ = 20

    if 'se13-aw' in the_competition:
        size_ = 16

    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2,
            height + 0.01,
            label,
            size=size_,
            ha='center', va='bottom')

rects = ax.patches
for index, (rect, label, system) in enumerate(zip(rects, labels, ordered_systems)):
    color = system2color[system]
    print(system, color)
    rect.set_edgecolor(color)
    rect.set_linewidth(10)

# add title
ax.set_title('$F_1$ development over the years for %s' % the_competition, fontsize=30)

# add legend
#'FS': 'mediumblue',
#'KB (S)': 'orange',
#'KB (U)': 'green',
#'Semi-S': 'red'

legend_elements = [Patch(facecolor='white', edgecolor='#0173B2', linewidth=8, label='FS'),
                   Patch(facecolor='white', edgecolor='#DE8F05', linewidth=8, label='KB (S)'),
                   Patch(facecolor='white', edgecolor='#029E73', linewidth=8, label='KB (U)'),
                   Patch(facecolor='white', edgecolor='#D55E00', linewidth=8, label='Semi-S'),]
lgd = ax.legend(handles=legend_elements, loc='center', fontsize=30, bbox_to_anchor=(1.1, 0.5))


# save plot
plt.savefig(output_path, bbox_extra_artists=(lgd,), bbox_inches='tight')

title = 'F1 development'

plot_df.to_pickle(data_path)

print('data saved to', data_path)
print('plot saved to', output_path)
