'''
nohup python -u plot_normalized_cross_correlation.py >& out &

author:
username J. username
Nov 5, 2014
username@gmail.com


load strokes

separate into list

choose sample_size random strokes

for each parameter (accel_x, ...)

  for each pair of strokes

    keep track of stroke_ID, label

    signal = parameter (accel_x, etc)

    center, normalize by sqrt(var) and mean stroke length

    add results to a table or matrix

plot matrix as heat map
'''

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt
import math
import random
import statistics

#infile_name = "/home/username/Desktop/home/data/segmented_flat.csv"
#infile_name = "~/home/data/segmented_flat.csv"
infile_name = "../data/segmented_flat.csv"

# for display purposes, should be a perfect square (25, 36, etc.)
#sample_size = 25
sample_size = 36

# set this based on average stroke length              
# BELOW, USE THE MEAN OF THE LENGTHS OF THE TWO STROKES FOR NORMALIZATION
#N_length_constant = 30


print("reading data...")

data = pd.read_csv(infile_name)
unique_labels = set(data['label'])
params = list(data.columns)[3:16]

# get a list of all strokes
stroke_ids = list(set(data['Stroke_ID']))

print("getting strokes")

all_strokes = []
stroke_lengths = []
for stroke_id in stroke_ids:
     new_stroke = data[data['Stroke_ID'] == stroke_id]
     all_strokes.append(new_stroke)
     stroke_lengths.append(len(new_stroke))

print("mean, median, stdev, variance of stroke lengths")
avg = statistics.mean(stroke_lengths)
print(avg)
print(statistics.median(stroke_lengths))
print(statistics.stdev(stroke_lengths))
print(statistics.variance(stroke_lengths))
plt.hist(stroke_lengths, bins = 50, color = 'b')
plt.vlines(avg, 0, 500, 'r')
plt.title("stroke lengths, mean = " + str(avg))
plt.savefig("figs/stroke_lengths.pdf")

for param in params:

     print(param)
     #print("labels are: " + str(unique_labels))

     # print(str(len(all_strokes)) + " strokes")

     print("getting first " + str(sample_size) + " strokes")

     # randomly sample from all strokes
#     strokes_sample = []
     strokes_sample = random.sample(all_strokes, sample_size)

#     for stroke_id in stroke_ids[:sample_size]:
#          strokes_sample.append(data[data['Stroke_ID'] == stroke_id])

     print(str(len(strokes_sample)) + " strokes")

     labels = []
     stroke_ids = []
     col_row_labels = []

     # also save timeseries for later
#     fig, ax = plt.subplots(sample_size, 1, subplot_index)
#     ax.set_title(param + ' time series')
     fig = plt.figure()
     fig.subplots_adjust(hspace=0.6, wspace=0.6)
     plot_pos = 1

     for stroke in strokes_sample:
          # uniq
          label = set(stroke.label).pop()
          stroke_id = set(stroke.Stroke_ID).pop()
          
          labels.append(label)
          stroke_ids.append(stroke_id)
          col_row_labels.append(label + "_" + str(stroke_id))

          # get the signal
          sig = np.array(stroke[param])
          ax1 = fig.add_subplot(int(math.sqrt(sample_size)),int(math.sqrt(sample_size)),plot_pos)
          ax1.set_title(label + "_" + str(stroke_id) + " " + param, size = 'small')

          ax1.plot(sig, 'r-')
          plot_pos = plot_pos + 1

     print("saving time series")
     plt.savefig('figs/' + param + '_time_series.pdf')
     plt.close()

     print(labels)
     print(stroke_ids)
     print(col_row_labels)

     normed_cross_correlations = np.zeros([sample_size, sample_size])
     cross_correlations = np.zeros([sample_size, sample_size])

     #for id1 in stroke_ids:
     #    for id2 in range(id1, len(stroke_ids)):
     print("finding cross-correlations")

     for i in range(0, len(stroke_ids)):
          id1 = int(stroke_ids[i])
          label1 = labels[i]

          print("stroke: " + str(id1))

          for j in range(i, len(stroke_ids)):
               id2 = int(stroke_ids[j])
               label2 = labels[j]

               # the raw signal
               sig1 = np.array(strokes_sample[i][param])
               sig2 = np.array(strokes_sample[j][param])

               # centered, normed
               avg1 = np.mean(sig1)
               sqrt_var1 = math.sqrt(np.var(sig1))
               sig1_scaled = (sig1 - avg1)/sqrt_var1

               avg2 = np.mean(sig2)
               sqrt_var2 = math.sqrt(np.var(sig2))
               sig2_scaled = (sig2 - avg2)/sqrt_var2

               sig1_length = len(sig1)
               sig2_length = len(sig2)

               # HERE, USE THE MEAN OF THE LENGTHS OF THE TWO STROKES FOR NORMALIZATION
               N_length_constant = statistics.mean([sig1_length, sig2_length])

               result = np.max(signal.correlate(sig1_scaled, sig2_scaled))/N_length_constant
               normed_cross_correlations[i,j] = result
               
               print("label1 " + label1 + " stroke_id1 " + str(id1))
               print("label2 " + label2 + " stroke_id2 " + str(id2))
               print("normed cross correlation " + str(result))
     
               # the raw cross-correlations
               cross_correlations[i,j] = np.max(signal.correlate(sig1, sig2))

     # save as .csv
     print("saving .csv files")

     np.savetxt("csvs/normed_cross_correlations.csv", normed_cross_correlations, delimiter = ",")
     np.savetxt("csvs/raw_cross_correlations.csv", cross_correlations, delimiter = ",")


     print("making heatmaps")


     # make heatmap of raw cross-correlations
     fig, ax = plt.subplots()
#     heatmap = ax.pcolor(cross_correlations)
     heatmap = ax.pcolormesh(cross_correlations, cmap=plt.cm.Blues)

     # put the major ticks at the middle of each cell, notice "reverse" use of dimension
     ax.set_yticks(np.arange(cross_correlations.shape[0])+0.5, minor=False)
     ax.set_xticks(np.arange(cross_correlations.shape[1])+0.5, minor=False)

     ax.set_xticklabels(col_row_labels, minor=False, rotation = 45, size = 'small')
     ax.set_yticklabels(col_row_labels, minor=False, size = 'small')
     ax.set_title('heatmap ' + param + ' raw cross-correlations', size = 'small')
     fig.colorbar(heatmap)
     #plt.show()
     plt.savefig('figs/heatmap ' + param + ' raw cross-correlations.pdf')
     plt.close()


     # make heatmap of normed cross-correlations
     fig, ax = plt.subplots()
#     heatmap = ax.pcolor(normed_cross_correlations)
     heatmap = ax.pcolormesh(normed_cross_correlations, cmap=plt.cm.Greens)
#     heatmap = ax.pcolormesh(data, cmap=plt.cm.Blues)


     # put the major ticks at the middle of each cell, notice "reverse" use of dimension
     ax.set_yticks(np.arange(normed_cross_correlations.shape[0])+0.5, minor=False)
     ax.set_xticks(np.arange(normed_cross_correlations.shape[1])+0.5, minor=False)

     ax.set_xticklabels(col_row_labels, minor=False, rotation = 45, size = 'small')
     ax.set_yticklabels(col_row_labels, minor=False, size = 'small')
     ax.set_title('heatmap ' + param + ' normed cross-correlations', size = 'small')

#     ax.set_xticklabels(col_row_labels, minor=False, rotation = 45)
#     ax.set_yticklabels(col_row_labels, minor=False)

#     ax.set_title('heatmap ' + param + ' normed cross-correlations')
     fig.colorbar(heatmap)
     #plt.show()
     plt.savefig('figs/heatmap ' + param + ' normed cross-correlations.pdf')
     plt.close()


     # also save timeseries of all strokes chosen




print("done")
