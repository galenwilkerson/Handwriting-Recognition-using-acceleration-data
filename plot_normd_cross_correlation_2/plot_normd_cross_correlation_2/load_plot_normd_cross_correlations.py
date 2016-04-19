'''
load the cross-correlations, plot them in a heat map

'''

print("Starting")

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt

infile_name = "./csvs/accel_x_avg_stroke_pair_normd_cross_corr.csv"
print("Reading data...")
data = pd.read_csv(infile_name)

param = "accel_x"

# make heat map, save
print("Making heatmap")

col_row_labels = list(data.columns.values[1:])
data_values = np.array(data.values[0:,1:], dtype = float)

# make heatmap of normed cross-correlations
fig, ax = plt.subplots()
heatmap = ax.pcolormesh(np.array(data_values, dtype = float), cmap=plt.cm.Reds)

# put the major ticks at the middle of each cell, notice "reverse" use of dimension
ax.set_yticks(np.arange(data_values.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(data_values.shape[1])+0.5, minor=False)

ax.set_xticklabels(col_row_labels, minor=False, rotation = 45, size = 'small')
ax.set_yticklabels(col_row_labels, minor=False, size = 'small')
ax.set_title('heatmap ' + param + ' label average normed cross-correlations', size = 'small')

fig.colorbar(heatmap)
#plt.show()
plt.savefig('figs/heatmap_' + param + '_average_normed_cross-correlations.pdf')
plt.close()



# try normalizing each row by the diagonal element

upper_triangular_data = np.triu(data_values)

# for each row, divide the row by the value of the diagonal element

row_normed_matrix = np.zeros(data_values.shape)
for i in range(0, len(upper_triangular_data)):
    diag_elt = upper_triangular_data[i][i]
    normed_row = upper_triangular_data[i] / diag_elt
    row_normed_matrix[i] = normed_row



# make heat map, save
print("Making normed triangular heatmap")

# make heatmap of normed cross-correlations
fig, ax = plt.subplots()
heatmap = ax.pcolormesh(np.array(row_normed_matrix, dtype = float), cmap=plt.cm.Reds)

# put the major ticks at the middle of each cell, notice "reverse" use of dimension
ax.set_yticks(np.arange(row_normed_matrix.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(row_normed_matrix.shape[1])+0.5, minor=False)

ax.set_xticklabels(col_row_labels, minor=False, rotation = 45, size = 'small')
ax.set_yticklabels(col_row_labels, minor=False, size = 'small')
ax.set_title('heatmap ' + param + ' label avg normed cross-corr., normed by diagonal', size = 'small')

fig.colorbar(heatmap)
#plt.show()
plt.savefig('figs/heatmap_' + param + '_diag_average_normed_cross-correlations.pdf')
plt.close()


