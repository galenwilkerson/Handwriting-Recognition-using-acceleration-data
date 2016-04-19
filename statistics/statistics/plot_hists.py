'''
run like:
> python2.7 -u test_plot_hists.py >& out &

load data

for each stroke, for each parameter

plot a hist of the parameter values

plot a hist of displacement values

perhaps:
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
#filename = "../data/stroke_data.pkl"

        pkl_file = open(filename, 'rb')
        stroke_data = cPickle.load(pkl_file)
         
        num_stats = len(stroke_data['e']) #accelx, accely, ... displacement(accelx), ...
        
        # initialize stroke data to list of lists
        # each list (by parameter) contains all of the data for this unique strokes parameter (for stats later)
        for current_label in stroke_data.keys():
                
                data_current_stroke = stroke_data[current_label]

                for j in range(0, num_stats):


                        if (j, num_stats/2):  # the standard stats

                                # the current parameter: accelx, accely, ... displacement(accelx), ...
                                data_current_param = data_current_stroke[j]

                                # find the statistics
                                mean = np.mean(data_current_param)
                                median = np.median(data_current_param)
                                minimum = np.min(data_current_param)
                                maximum = np.max(data_current_param)

                                # the histogram of the data
                                n, bins, patches = plt.hist(data_current_param, 100, normed=1, facecolor='green', alpha=0.75)

                                # add a 'best fit' line
                                #                        y = mlab.normpdf( bins, mu, sigma)
                                #                        l = plt.plot(bins, y, 'r--', linewidth=1)

                                plt.xlabel(current_label)
                                plt.ylabel('Probability')
                                plt.title(current_label + '_'  + '_parameter_' + str(j))
                                #                        plt.axis([40, 160, 0, 0.03])
                                #                        plt.grid(True)
                        
                                #                        plt.show()
                                plt.savefig('../figs/' + current_label + '_'  + '_parameter_' + str(j) + '.pdf')
                                plt.close()

                        # and displacements
                        else:

                                mean_disp = np.mean(displacements)
                                median_disp = np.median(displacements)
                                min_disp = np.min(displacements)
                                max_disp = np.max(displacements)

                                #hist_disp = np.histogram(data_current_param)


                                # the histogram of the data
                                n, bins, patches = plt.hist(displacements, 100, normed=1, facecolor='green', alpha=0.75)

                                # add a 'best fit' line
                                #                        y = mlab.normpdf( bins, mu, sigma)
                                #                        l = plt.plot(bins, y, 'r--', linewidth=1)

                                plt.xlabel(current_label)
                                plt.ylabel('Probability')
                                plt.title(current_label + '_displacements_'  + '_parameter_' + str(j))
                                #                        plt.axis([40, 160, 0, 0.03])
                                #                        plt.grid(True)
                                
                                #                        plt.show()
                        plt.savefig('../figs/' + current_label + '_displacements_'  + '_parameter_' + str(j) + '.pdf')
                                plt.close()



