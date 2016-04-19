'''
load average normed cross correlation

plot as heat map
'''



print("Starting")

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt
import math
import random
#import statistics
import pickle


infile_name = "./csvs/accel_x_avg_stroke_pair_normd_cross_corr.csv"
print("Reading data...")
data = pd.read_csv(infile_name)

# make heat map, save
print("Making heatmap")

# make heatmap of normed cross-correlations
fig, ax = plt.subplots()
#heatmap = ax.pcolormesh(np.array(data.as_matrix, dtype = float), cmap=plt.cm.Reds)
heatmap = ax.pcolormesh(np.array(data.as_matrix), cmap=plt.cm.Reds)

# put the major ticks at the middle of each cell, notice "reverse" use of dimension
#ax.set_yticks(np.arange(avg_normed_cross_correlations.shape[0])+0.5, minor=False)
#ax.set_xticks(np.arange(avg_normed_cross_correlations.shape[1])+0.5, minor=False)

ax.set_xticklabels(col_row_labels, minor=False, rotation = 45, size = 'small')
ax.set_yticklabels(col_row_labels, minor=False, size = 'small')
ax.set_title('heatmap ' + param + ' label average normed cross-correlations', size = 'small')

fig.colorbar(heatmap)
plt.show()
#plt.savefig('figs/heatmap_' + param + '_average_normed_cross-correlations.pdf')
plt.close()
