# quick histogram and descriptive statistics of stroke lengths

import matplotlib.pyplot as plt
import numpy as np


# load file

# find histogram

# plot it

filename = "../output/stroke_label_lengths.csv"

import csv

#infile = open('eggs.csv', 'rb') as csvfile

from numpy import genfromtxt

my_data = genfromtxt(filename, delimiter=',')

#my_hist = np.histogram(my_data[:,1])

plt.hist(my_data[:,1], bins = 50)

plt.show()
