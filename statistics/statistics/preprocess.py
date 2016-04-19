'''
Function to pre-process for SVM (or other method)

Find basic statistics

Basically, does "feature expansion" for SVM

Code to classify using SVM

Steps:

- read data

- for each stroke, for each parameter, get data statistics
  - distance between points (normalize?)
  - mean, median, mode distance
  - mean, median, mode value
  - stroke_length
- build X

- multiply X by itself -> X^2 (feature expansion in prep for kernel method / SVM)
- center and normalize X^2 by mean and standard deviation
- vectorize X^2 (10 x 10 -> 100 dimensions)
- concatenate with input X -> 110 dimensions

- map stroke values to integers:  K1 becomes int(K), 1
- return array of vectors, each vector having the data concatenated with the stroke value

'''

import pandas as pd
import numpy as np
#from sklearn.svm import SVC
from scipy import interpolate
from sklearn import preprocessing  # for scale (centering and normalizing vectors)
import pickle
import cPickle

# read in pickle file containing stroke data
# return list of strokes, 
# and list of 'feature expanded', spline-interpolated, resampled values (for each parameter - accelX, accelY, etc.)
# inputs are name of pkl file and number of resamplings from spline
def preprocess(filename, num_resamplings = 25):

	# read data
	#filename = "../data/MarieTherese_jul31_and_Aug07_all.pkl"

	pkl_file = open(filename, 'rb')
        data1 = cPickle.load(pkl_file)
        num_strokes = len(data1)

        # get the unique stroke labels, map to class labels (ints) for later using dictionary
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

	# - smooth data
	# 	for each stroke, get the vector of data, smooth/interpolate it over time, store sampling from smoothed signal in vector
	# - sample at regular intervals (1/30 of total time, etc.) -> input vector X


	num_params = len(data1[0][1][0]) #accelx, accely, etc.
	#num_params = 16 #accelx, accely, etc.

        # re-sample the interpolated spline this many times (25 or so seems ok, since most letters have this many points)
	#num_resamplings = 25 

        # the square of the number of resamplings, for shaping the X_2 into a vector
	num_resamplings_2 = num_resamplings * num_resamplings 

        # build an output array large enough to hold the vectors for each stroke and the (unicode -> int) stroke value (1 elts)
        output_array = np.zeros((num_strokes, (num_resamplings_2 + num_resamplings) * num_params + 2))
        print output_array.size

        print filename
        print num_params
        print num_resamplings_2
        print

	for i in range(0, num_strokes):
	
		X_matrix = np.zeros((num_params, num_resamplings)) # the array to store in

                # the array to store reshaped resampled vector in
		X_2_vector_scaled = np.zeros((num_params, num_resamplings_2)) 

                # the array to store the above 2 concatenated
		concatenated_X_X_2 = np.zeros((num_params, num_resamplings_2 + num_resamplings)) 

		# for each parameter (accelX, accelY, ...)

                # map the unicode character to int
                #print("curr_stroke")
                #print(data1[i][0])
#		curr_stroke = np.zeros(2)
#                curr_stroke_temp = np.fromstring(data1[i][0], dtype=np.uint8)
#                curr_stroke[0] = curr_stroke_temp[0]
#                if(len(curr_stroke_temp) == 2):
#                        curr_stroke[1] = curr_stroke_temp[1]
 
                curr_stroke_val = stroke_dict[data1[i][0]]
                                        
                #print(len(curr_stroke))
                #print(curr_stroke[0])
                #print(curr_stroke[1])

		curr_data = data1[i][1]
                stroke_length = len(curr_data)

                # fix if too short for interpolation - pad current data with 3 zeros
                if(len(curr_data) <= 3):
                        curr_data = np.concatenate([curr_data, np.zeros((3,num_params))])

		time = np.arange(0, len(curr_data), 1) # the sample 'times' (0 to number of samples)
		time_new = np.arange(0, len(curr_data), float(len(curr_data))/num_resamplings) # the resampled time points

		for j in range(0, num_params): # iterate through parameters

			signal = curr_data[:,j] # one signal (accelx, etc.) to interpolate

                        # find distances between subsequent points
                        # diffs = signal - 

                        

'''

			X_matrix[j] = preprocessing.scale(resampled_data)

			# while we're at it, square vector of resampled data to get a matrix, vectorize the matrix, and store
			#  for each X in list, multiply X by itself -> X_2
			#- vectorize X^2 (e.g. 10 x 10 -> 100 dimensions)
			X_2_matrix = np.outer(resampled_data, resampled_data) # temp matrix for outer product
			X_2_vector = np.reshape(X_2_matrix, num_resamplings_2) # reshape into a vector

			#- center and normalize X^2 by mean and standard deviation
			X_2_vector_scaled[j] = preprocessing.scale(X_2_vector) 

			#- concatenate with input X -> 110 dimensions
			concatenated_X_X_2[j] = np.concatenate([X_matrix[j], X_2_vector_scaled[j]])
'''

                # NOTE, THIS SHOULD REALLY JUST BE A BIG VECTOR FOR EACH STROKE, SO RESHAPE BEFORE ADDING TO OUTPUT LIST
                # ALSO, THE STROKE VALUE SHOULD BE ADDED
                this_sample = np.concatenate((np.reshape(concatenated_X_X_2, -1), np.array([stroke_length]), np.array([curr_stroke_val])))
                concatenated_samples = np.reshape(this_sample, -1)

                # ADD TO OUTPUT ARRAY
                output_array[i] = concatenated_samples
        
        print(output_array.size)
        
#	return(strokes, concatenated_X_X_2_list)
	return(output_array)


