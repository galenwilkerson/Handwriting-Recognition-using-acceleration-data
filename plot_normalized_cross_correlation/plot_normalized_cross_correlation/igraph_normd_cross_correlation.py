'''
Just handle strokes as a graph, and weights as average normalized cross-correlation.

Find the normalized cross correlation between all pairs of strokes

so we can compare same strokes' cross-correlations to those of other strokes.


Try again:

create graph using strokes

for each stroke

  for each other stroke

    compute the max normalized cross correlation

'''


import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt
import math
import random
import statistics
import igraph

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
unique_labels = list(set(data['label']))
params = list(data.columns)[3:16]

# get a list of all strokes
stroke_ids = list(set(data['Stroke_ID']))

print("getting strokes")

all_strokes = []
stroke_lengths = []
g = igraph.Graph()

for stroke_id in stroke_ids:
     new_stroke = data[data['Stroke_ID'] == stroke_id]
     all_strokes.append(new_stroke)
     stroke_lengths.append(len(new_stroke))
     g.add_vertex(stroke_id)



for stroke_id in stroke_ids:
    for stroke_id2 in range(stroke_id, len(stroke_ids)):
        g.add_edges((stroke_id, stroke_id2))







