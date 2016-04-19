'''
load data

for each stroke, for each parameter

get the statistical information about the stroke:
mean
median
min 
max
num points

statistics for distances:
distances between points
mean distance
max
min
median
'''


import pandas as pd
import numpy as np
#from sklearn.svm import SVC
from scipy import interpolate
from sklearn import preprocessing  # for scale (centering and normalizing vectors)
import pickle
import cPickle

# input: filename of stroke data

# output: array containing statistics about each stroke
def get_stats(filename):

    	# read data
	#filename = "../data/MarieTherese_jul31_and_Aug07_all.pkl"

	pkl_file = open(filename, 'rb')
        data1 = cPickle.load(pkl_file)
        num_strokes = len(data1)

        # get the unique stroke labels, 
        # map to class labels (ints) for later using dictionary
        stroke_dict = dict()
        value_index = 0
        for i in range(0,num_strokes):
                current_key = data1[i][0]
                if current_key not in stroke_dict:
                        stroke_dict[current_key] = value_index
                        value_index = value_index + 1

        # save the dictionary to file, for later use
        dict_filename = "../data/stroke_label_mapping.pkl"
        dict_file = open(dict_filename, 'wb')
        pickle.dump(stroke_dict, dict_file)

        num_params = len(data1[0][1][0]) #accelx, accely, etc.

        # the number of statistics to collect
        #num_stats = 


        # for each stroke, for each parameters, store:
        # stroke label, stroke length, stroke statistics
        output_array = np.zeros(num_strokes, num_params, num_stats)

        for i in range(0, num_strokes):

                # get the label
                current_label = data1[i][0]
                current_data = data1[i][1]

                stroke_length = len(current_data)

                for j in range(0, num_params):

                        data_current_param = current_data[:,j]

                        # find the statistics
                        mean = np.mean(data_current_param)
                        median = np.median(data_current_param)
                        minimum = np.min(data_current_param)
                        maximum = np.max(data_current_param)

                        # now find displacement statistics
                        displacements = np.diff(data_current_param)

                        mean_disp = np.mean(displacements)
                        median_disp = np.median(displacements)
                        min_disp = np.min(displacements)
                        max_disp = np.max(displacements)
