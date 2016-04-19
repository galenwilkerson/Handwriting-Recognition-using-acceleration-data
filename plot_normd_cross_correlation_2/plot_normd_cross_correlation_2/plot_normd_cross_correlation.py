'''
For all pairs of strokes, find the max normed cross-correlation.

Store in an array.

Then, want to know average cross correlation for each pair.

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

'''
function to find cross-correlations, plot heat maps, and save them
'''
def find_cross_corrs_plot_save(param):
     print("Finding max normalized cross-correlations...")
     print(param)

     for stroke_id1 in stroke_ids:

          if(stroke_id1 % 10 == 0):
               print("Stroke " + str(stroke_id1))
               
          label1 = set(all_strokes[stroke_id1]['label']).pop()
          label1_id = label_dict[label1]

          sig1 = np.array(all_strokes[stroke_id1][param])
          sig1_length = len(sig1)

          # centered, normed
          avg1 = np.mean(sig1)
          sqrt_var1 = math.sqrt(np.var(sig1))
          sig1_scaled = (sig1 - avg1)/sqrt_var1

          # JUST DO THEM ALL, DON'T BE 'CLEVER', savings aren't that great anyway
          for stroke_id2 in stroke_ids:
        
               label2 = set(all_strokes[stroke_id2]['label']).pop()
               label2_id = label_dict[label2]

               # get the signal
               sig2 = np.array(all_strokes[stroke_id2][param])
               sig2_length = len(sig2)

               # center and norm
               avg2 = np.mean(sig2)
               sqrt_var2 = math.sqrt(np.var(sig2))
               sig2_scaled = (sig2 - avg2)/sqrt_var2

               # HERE, USE THE MEAN OF THE LENGTHS OF THE TWO STROKES FOR NORMALIZATION
               N_length_constant = np.mean([sig1_length, sig2_length])

               # compute normed cross-correlation
               result = np.max(signal.correlate(sig1_scaled, sig2_scaled))/N_length_constant
        
               max_normd_cross_correlations[stroke_id1][stroke_id2] = result

               # and now by label
               sum_stroke_pair_normd_cross_correlations[label1_id][label2_id] =  result + sum_stroke_pair_normd_cross_correlations[label1_id][label2_id] 

               # and the number of stroke pairs
               num_strokes_pairs[label1_id][label2_id] = num_strokes_pairs[label1_id][label2_id]  + 1


     # find the average
     avg_stroke_pair_normd_cross_correlations = sum_stroke_pair_normd_cross_correlations / num_strokes_pairs

     #print(num_strokes_pairs)
     #print
     #print(sum_stroke_pair_normd_cross_correlations)
     #print
     #print(avg_stroke_pair_normd_cross_correlations)


     # SAVE THESE ARRAYS, just make pandas dataframes
     print("Saving .csvs")
     col_row_labels = label_dict.keys()
     max_normd_cross_correlations_df = pd.DataFrame(max_normd_cross_correlations)
     num_stroke_pairs_df = pd.DataFrame(num_strokes_pairs, index = col_row_labels, columns = col_row_labels)
     sum_stroke_pair_normd_cross_correlations_df = pd.DataFrame(sum_stroke_pair_normd_cross_correlations, index = col_row_labels, columns = col_row_labels)
     avg_stroke_pair_normd_cross_correlations_df = pd.DataFrame(avg_stroke_pair_normd_cross_correlations, index = col_row_labels, columns = col_row_labels)
     
     max_normd_cross_correlations_df.to_csv("csvs/"+param+"_max_normd_cross_correlations.csv", na_rep = 0)
     num_stroke_pairs_df.to_csv("csvs/"+param+"_num_stroke_pairs.csv", na_rep = 0)
     sum_stroke_pair_normd_cross_correlations_df.to_csv("csvs/"+param+"_sum_stroke_pair_cross_corr.csv", na_rep = 0)
     avg_stroke_pair_normd_cross_correlations_df.to_csv("csvs/"+param+"_avg_stroke_pair_normd_cross_corr.csv", na_rep = 0)



     # make heat map, save
     print("Making heatmap")

     # make heatmap of normed cross-correlations
     fig, ax = plt.subplots()
     heatmap = ax.pcolormesh(np.array(avg_stroke_pair_normd_cross_correlations, dtype = float), cmap=plt.cm.Reds)

     # put the major ticks at the middle of each cell, notice "reverse" use of dimension
     ax.set_yticks(np.arange(avg_stroke_pair_normd_cross_correlations.shape[0])+0.5, minor=False)
     ax.set_xticks(np.arange(avg_stroke_pair_normd_cross_correlations.shape[1])+0.5, minor=False)

     ax.set_xticklabels(col_row_labels, minor=False, rotation = 45, size = 'small')
     ax.set_yticklabels(col_row_labels, minor=False, size = 'small')
     ax.set_title('heatmap ' + param + ' label average normed cross-correlations', size = 'small')

     fig.colorbar(heatmap)
     #plt.show()
     plt.savefig('figs/heatmap_' + param + '_average_normed_cross-correlations.pdf')
     plt.close()




     # try normalizing each row by the diagonal element
     upper_triangular_data = np.triu(avg_stroke_pair_normd_cross_correlations)

     # for each row, divide the row by the value of the diagonal element

     row_normed_matrix = np.zeros(avg_stroke_pair_normd_cross_correlations.shape)
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






#infile_name = "../data/segmented_flat.csv"
infile_name = "./segmented_flat.csv"
print("Reading data...")
data = pd.read_csv(infile_name)
unique_labels = list(set(data['label'])) 
params = list(data.columns)[3:16]

# get a list of all strokes
stroke_ids = list(set(data['Stroke_ID']))[:10]
num_strokes = len(stroke_ids)

print("Getting strokes")

all_strokes = []
stroke_lengths = []
stroke_labels = []
for stroke_id in stroke_ids:
     new_stroke = data[data['Stroke_ID'] == stroke_id]
     all_strokes.append(new_stroke)
     stroke_lengths.append(len(new_stroke))
     stroke_labels.append(set(new_stroke['label']).pop())

# make an array to store all of the max normalized cross-correlations
max_normd_cross_correlations = np.zeros((num_strokes, num_strokes))

# make another array to store the totals for each stroke label pair
sum_stroke_pair_normd_cross_correlations = np.zeros((len(unique_labels), len(unique_labels)))

# and the number of stroke pairs
num_strokes_pairs = np.zeros((len(unique_labels), len(unique_labels)))


#set up a dictionary to look up labels
label_dict = dict.fromkeys(unique_labels)
i = 0
for key in label_dict:
    label_dict[key] = i
    i = i + 1

from joblib import Parallel, delayed
#Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
Parallel(n_jobs=-1)(delayed(find_cross_corrs_plot_save)(param) for param in params)

#param = "accel_x"
#for param in params:
#     find_cross_corrs_plot_save(param)
     

