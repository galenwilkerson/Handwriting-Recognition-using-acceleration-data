'''
Prediction / classification:

- load model strokes for each label

- load unknown/test data

- for each unknown stroke U

	- for each model stroke M_L

		- find cross-correlation of M_L with U -> store score in array

		- classify U as L with highest cross-correlation

- save predictions

run as:
python -u <thisfile>.py >& out &

needs figs/ folder
'''

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt
import csv

param = "accel_x"

# load model strokes
model_strokes_filename = param + " model_strokes.csv"

all_data = []
f = open(model_strokes_filename)
data_file = csv.reader(f)

for row in data_file:
    all_data.append(row)


# separate strokes into labels and data
model_strokes_labels = []
model_strokes_data = []
for i in range(0, len(all_data), 2):
    length = len(all_data[i+1])
    model_strokes_labels.append(all_data[i+1][0])
    model_strokes_data.append(np.array(all_data[i+1][2:], dtype=float))
    


# load test/prediction data
test_strokes_filename = param + " test_strokes.csv"

all_data = []
f = open(test_strokes_filename)
data_file = csv.reader(f)

for row in data_file:
    test_data.append(row)

# for each new stroke, find the label having highest cross-correlation
for new_stroke in test_data:
    max_xcorr = -1e100
    max_xcorr_label = ""
    index_max_xcorr = -1
    for i in range(0, len(model_strokes_data)):
        temp_xcorr = signal.correlate(new_stroke, model_strokes_data[i])
        if temp_xcorr > max_xcorr:
            max_xcorr = temp_xcorr
            index_max_xcorr = i


    max_xcorr_label = model_strokes_labels[index_max_xcorr]




