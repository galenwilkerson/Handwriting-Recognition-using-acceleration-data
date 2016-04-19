'''
nohup python -u -O plot_average_normalized_cross_correlation.py >& out &

Plot the average of the normalized cross-correlation
between each unique label.

author:
username J. username
Nov 5, 2014
username@gmail.com

---

load strokes

find the num_labels

store the stroke_id and label of each stroke

dict(num_strokes_each_label) = find the number of strokes with each label


for each parameter:

  create array to store sums of cross_correlations between labels
  sums_this_label_pair = zeros([|num_labels|, |num_labels|])

  create array to store number of cross_correlations for each label_pair
  num_strokes_this_label_pair = zeros([|num_labels|, |num_labels|])

  create array to store final averages of cross_correlations between labels
  averages_this_label_pair = zeros([|num_labels|, |num_labels|])

  find numbers of strokes for each combination of unique labels:
  for each each label
    for each each other label
      num_strokes_this_label_pair = num_strokes_each_label[label1] * num_strokes_each_label[label2]

  find sums for each combination of unique labels:
  for each individual stroke, 
    for each other individual stroke
      get the labels of each
      find the normalized cross-correlation
        add value to sums_this_label_pair[label1][label2]

  find averages for each combination of unique labels:
  for each each label1
    for each each other label2
      averages_this_label_pair = 
         sum_this_label_pair[label1][label2] / 
         num_strokes_this_label_pair[label1][label2]

  create heat map by unique label pairs, save figure

'''

print("starting")

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt
import math
import random
#import statistics
import pickle

# load .csv version
#infile_name = "/home/username/Desktop/home/data/segmented_flat.csv"
infile_name = "../data/segmented_flat.csv"
#infile_name = "~/Desktop/home/data/segmented_flat.csv"
data = pd.read_csv(infile_name)

# FOR TESTING, ONLY USE 1ST 100 STROKES
data = data[data['Stroke_ID'] < 10]

# faster version using pickle
# infile_name = "./segmented_flat.pkl"
# print("reading data...")
# file = open("segmented_flat.pkl", "rb")
# data = pickle.load(file)
# file.close()


unique_labels = list(set(data['label']))
num_labels = len(unique_labels)

params = list(data.columns)[3:16]

# lists of all stroke ids and labels
stroke_ids = list(set(data['Stroke_ID']))


indiv_stroke_labels = []

print("getting strokes")   # FASTER USING PANDAS OR SOMETHING THAT DOES SUBSETTING/SPLITTING?

all_strokes = []
stroke_lengths = []
num_strokes_each_label =  dict.fromkeys(unique_labels, 0)
for stroke_id in stroke_ids:
     new_stroke = data[data['Stroke_ID'] == stroke_id]
     label = set(new_stroke.label).pop()
     indiv_stroke_labels.append(label)
     all_strokes.append(new_stroke)
     stroke_lengths.append(len(new_stroke))
     num_strokes_each_label[label] = num_strokes_each_label[label] + 1

num_strokes = len(all_strokes)

print(str(num_strokes) + " strokes")

print("strokes per label: ")
print(num_strokes_each_label)

# 2-D dictionary to store label pair counts
num_strokes_this_label_pair = dict()

# do this once, count of label pair sizes - CHECK, HAD INCORRECT VALUES!! **********
for i in range(0, len(unique_labels)):
    label1 = unique_labels[i]

    # init 2nd dimension of 2-D dictionary to 0s
    num_strokes_this_label_pair[label1] = dict.fromkeys(unique_labels, 0)
    
    for j in range(0, len(unique_labels)):
        label2 = unique_labels[j]
        num_strokes_this_label_pair[label1][label2] = num_strokes_each_label[label1] * num_strokes_each_label[label2]


# save num strokes per pair as .csv file for review later
print("saving num strokes per pair as .csv")

# convert dictionary to Pandas DataFrame for saving and plotting
num_strokes_per_pair = pd.DataFrame.from_dict(num_strokes_this_label_pair, dtype =  float)

# DOUBLE-CHECK THAT DIAGONALS ARE 1 
num_strokes_per_pair.to_csv("csvs/num_strokes_per_pair.csv", na_rep = 0)


# DEBUG:
params = params[:1]


for param in params:

     print("processing " + param)

     # 2-D dictionary to store pair correlation sums for average computation
     sums_this_label_pair = dict()

     # 2-D dictionary to store results for average computation
     averages_this_label_pair = dict()

     # init 2nd dimension of 2-D dictionaries to 0s
     print("initializing results dictionaries")

     for i in range(0, len(unique_labels)):
          label1 = unique_labels[i]
          sums_this_label_pair[label1] = dict.fromkeys(unique_labels, 0)
          averages_this_label_pair[label1] = dict.fromkeys(unique_labels, 0)
     
     print("finding normed cross-correlations... takes some time...")


     for i in range(0, len(all_strokes)):
# FOR TESTING
#     for i in range(0, 2):
          stroke1 = all_strokes[i]
          stroke_id1 = set(stroke1.Stroke_ID).pop()
          label1 = set(stroke1.label).pop()
          
          print("Stroke: " + str(stroke_id1) + " label: " + label1)

          sig1 = np.array(stroke1[param])

          avg1 = np.mean(sig1)
          sqrt_var1 = math.sqrt(np.var(sig1))
          sig1_scaled = (sig1 - avg1)/sqrt_var1


          for j in range(i, len(all_strokes)):
#  FOR TESTING
#          for j in range(i, 3):
               stroke2 = all_strokes[j]          
               stroke_id2 = set(stroke2.Stroke_ID).pop()
               label2 = set(stroke2.label).pop()

               print("Stroke: " + str(stroke_id2) + " label: " + label2)

               sig2 = np.array(stroke2[param])
        
               avg2 = np.mean(sig2)
               sqrt_var2 = math.sqrt(np.var(sig2))
               sig2_scaled = (sig2 - avg2)/sqrt_var2

               N_length_constant = float(len(sig1) + len(sig2))/2.0
              

               # SEEMS TO BE A BUG IN THE CROSS CORRELATION (A STROKE WITH ITSELF SHOULD BE 1)
               normed_cross_corr = np.max(signal.correlate(sig1_scaled, sig2_scaled))/N_length_constant
               
               print("normed cross correlation " + str(normed_cross_corr))


               # PROBLEM HERE??  *************

               sums_this_label_pair[label1][label2] = sums_this_label_pair[label1][label2] + normed_cross_corr





     # find averages of normed cross-correlations for each label pair
     for i in range(0, len(unique_labels)):
          label1 = unique_labels[i]
    
          for j in range(0, len(unique_labels)):
               label2 = unique_labels[j]

               averages_this_label_pair[label1][label2] = float(sums_this_label_pair[label1][label2])/num_strokes_this_label_pair[label1][label2]


     # save sums as .csv file for review later
     print("saving sums of cross-correlations as .csv")

     # convert dictionary to Pandas DataFrame for saving and plotting
     sum_normed_cross_correlations = pd.DataFrame.from_dict(sums_this_label_pair, dtype =  float)

     # DOUBLE-CHECK THAT DIAGONALS ARE 1 
     sum_normed_cross_correlations.to_csv("csvs/"+param+"_sum_normed_cross_correlations.csv", na_rep = 0)


     # save averages as .csv file for review later
     print("saving avg cross-correlations as .csv")

     # convert dictionary to Pandas DataFrame for saving and plotting
     avg_normed_cross_correlations = pd.DataFrame.from_dict(averages_this_label_pair, dtype =  float)

     # DOUBLE-CHECK THAT DIAGONALS ARE 1 
     avg_normed_cross_correlations.to_csv("csvs/"+param+"_avg_normed_cross_correlations.csv", na_rep = 0)

     print("avg_normed_cross_correlations.columms")
     print(avg_normed_cross_correlations.columns.tolist())

     print("avg_normed_cross_correlations.index")
     print(avg_normed_cross_correlations.index.tolist())

     col_row_labels = avg_normed_cross_correlations.index.tolist()

     # make heat map, save
     print("making heatmap")

     # make heatmap of normed cross-correlations
     fig, ax = plt.subplots()
     heatmap = ax.pcolormesh(np.array(avg_normed_cross_correlations, dtype = float), cmap=plt.cm.Reds)

     # put the major ticks at the middle of each cell, notice "reverse" use of dimension
     ax.set_yticks(np.arange(avg_normed_cross_correlations.shape[0])+0.5, minor=False)
     ax.set_xticks(np.arange(avg_normed_cross_correlations.shape[1])+0.5, minor=False)

     ax.set_xticklabels(col_row_labels, minor=False, rotation = 45, size = 'small')
     ax.set_yticklabels(col_row_labels, minor=False, size = 'small')
     ax.set_title('heatmap ' + param + ' label average normed cross-correlations', size = 'small')

     fig.colorbar(heatmap)
     #plt.show()
     plt.savefig('avg_normed_corr_figs/heatmap_' + param + '_average_normed_cross-correlations.pdf')
     plt.close()


print("done!")
   

