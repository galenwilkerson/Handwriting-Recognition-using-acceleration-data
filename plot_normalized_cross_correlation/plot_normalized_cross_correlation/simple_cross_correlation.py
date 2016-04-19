
# just look at normed cross correlation of two strokes

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt
import math
import random
import statistics

infile_name = "/home/username/Desktop/home/data/segmented_flat.csv"
#infile_name = "~/Desktop/home/data/segmented_flat.csv"


# set this based on average stroke length
N_length_constant = 30


print("reading data...")

data = pd.read_csv(infile_name)
unique_labels = set(data['label'])
params = list(data.columns)[3:16]

# get a list of all strokes
stroke_ids = list(set(data['Stroke_ID']))


stroke_1 = data[data['Stroke_ID'] == 1000]
stroke_2 = data[data['Stroke_ID'] == 500]

sig1 = np.array(stroke_1['gyr_z'])
sig2 = np.array(stroke_2['gyr_z'])

sig1_centered = sig1 - np.mean(sig1)
sig1_normed = sig1 / math.sqrt(np.var(sig1))
time1 = range(0, len(sig1))

sig2_centered = sig2 - np.mean(sig2)
sig2_normed = sig2 / math.sqrt(np.var(sig2))
time2 = range(0, len(sig2))
N = statistics.mean([len(sig1), len(sig2)])
normed_correlation = signal.correlate(sig1_normed, sig2_normed)/N

#plt.plot(time1, sig1, time2, sig2)
#plt.plot(signal.correlate(sig1, sig2), 'r')
#plt.show()

#plt.plot(time1, sig1_normed, time2, sig2_normed)
plt.plot(normed_correlation, 'r')

plt.show()
