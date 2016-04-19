'''
run like:
> python2.7 -u test_plot_hists.py >& out &

load data

for each stroke, for each parameter

plot a hist of the parameter values

plot a hist of displacement values

get the statistical information about the stroke, save to disk
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


#import pandas as pd
import numpy as np
#from sklearn.svm import SVC
#from scipy import interpolate
#from sklearn import preprocessing  # for scale (centering and normalizing vectors)
import pickle
import cPickle
import matplotlib.pyplot as plt

# input: filename of stroke data

# output: array containing statistics about each stroke
def plot_hists(filename):

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
        #        output_array = np.zeros(num_strokes, num_params, num_stats)

        # dict to store data
        #stroke_data = dict.fromkeys(stroke_dict)
        stroke_data = dict.fromkeys(stroke_dict.keys())
        
        # initialize stroke data to list of lists
        # each list (by parameter) contains all of the data for this unique strokes parameter (for stats later)
        for key in stroke_data.keys():
                stroke_data[key] = []
                for j in range(0, num_params * 2):  # store both stats and displacement stats
                        stroke_data[key].append([])
                        
        print("done init")

        for i in range(0, num_strokes):

                # get the label
                current_label = data1[i][0]
                current_data = data1[i][1]

                stroke_length = len(current_data)

                for j in range(0, num_params):

                        data_current_param = current_data[:,j]

                        (stroke_data[current_label])[j].extend(data_current_param.tolist())

                        # now find displacement statistics
                        displacements = np.diff(data_current_param)

                        (stroke_data[current_label])[j + num_params].extend(displacements.tolist())


        # save stroke data to file
        filename = "../data/stroke_data.pkl"
        out_file = open(filename, 'wb')
        pickle.dump(stroke_data, out_file)
        out_file.close()

        print("done")

'''
                        # find the statistics
                        mean = np.mean(data_current_param)
                        median = np.median(data_current_param)
                        minimum = np.min(data_current_param)
                        maximum = np.max(data_current_param)

                        #  hist = np.histogram(data_current_param)
                        
                        # the histogram of the data
                        n, bins, patches = plt.hist(data_current_param, 50, normed=1, facecolor='green', alpha=0.75)

                        # add a 'best fit' line
#                        y = mlab.normpdf( bins, mu, sigma)
#                        l = plt.plot(bins, y, 'r--', linewidth=1)

                        plt.xlabel(current_label)
                        plt.ylabel('Probability')
                        plt.title(current_label + '_' + str(i) + '_parameter_' + str(j))
                        #                        plt.axis([40, 160, 0, 0.03])
                        #                        plt.grid(True)
                        
                        #                        plt.show()
                        plt.savefig('../figs/' + current_label + '_' + str(i) + '_parameter_' + str(j) + '.pdf')
                        plt.close()

# and displacements

                        mean_disp = np.mean(displacements)
                        median_disp = np.median(displacements)
                        min_disp = np.min(displacements)
                        max_disp = np.max(displacements)

                        #hist_disp = np.histogram(data_current_param)


                        # the histogram of the data
                        n, bins, patches = plt.hist(displacements, 50, normed=1, facecolor='green', alpha=0.75)

                        # add a 'best fit' line
#                        y = mlab.normpdf( bins, mu, sigma)
#                        l = plt.plot(bins, y, 'r--', linewidth=1)

                        plt.xlabel(current_label)
                        plt.ylabel('Probability')
                        plt.title(current_label + '_displacements_' + str(i) + '_parameter_' + str(j))
#                        plt.axis([40, 160, 0, 0.03])
#                        plt.grid(True)
                        
#                        plt.show()
                        plt.savefig('../figs/' + current_label + '_displacements_' + str(i) + '_parameter_' + str(j) + '.pdf')
                        plt.close()
'''


