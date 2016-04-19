'''

load strokes (either model strokes or individual)

for each pair, find their max(corrcoeff)

plot as a heat map

'''


import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt

infile_name = "../data/segmented_flat.csv"
sample_size = 10

print("reading data...")

data = pd.read_csv(infile_name)
unique_labels = set(data['label'])
params = list(data.columns)[3:16]


print("labels are: " + str(unique_labels))

# get a list of all strokes
stroke_ids = set(data['Stroke_ID'])

all_strokes = []
for stroke_id in stroke_ids:
    all_strokes.append(data[data['Stroke_ID'] == stroke_id])

print(str(len(all_strokes)) + " strokes")


# find corrcoeff for each pair of strokes

# store max correlation results in multidimensional dictionary
correlation_results = dict()
for param in params:
    print("correlating " + param)
    # add dictionary of results for this stroke
    correlation_results[param] = dict()
    for stroke_i in all_strokes:
        print("stroke " + str(set(stroke_i.Stroke_ID).pop()))
        i_label = set(stroke_i.label).pop()
        correlation_results[param][i_label] = dict()
        sig1 = stroke_i[param]
        for stroke_j in all_strokes:
            j_label = set(stroke_j.label).pop()
            sig2 = stroke_j[param]
            cor = max(signal.correlate(sig1, sig2)) # corr_coeff = numpy.corr
            correlation_results[param][i_label][j_label] = cor;
        
