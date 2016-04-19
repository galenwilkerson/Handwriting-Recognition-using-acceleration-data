'''
Function to pre-process for SVM (or other method)

Basically, does "feature expansion" for SVM

Code to classify using SVM

Steps:

- read data
- smooth data (here using splines from scipy)

- fit splines
- find 1st and second derivatives
- find 0 points of second derivative
- split curves at 0 points:  A, C
- find mid-point: B
- find radius of curvature for A, B, C
- construct X vector from radius of curvature 
- center and normalize X

- map stroke values to integers:  K1 becomes int(K), 1
- return array of X vectors, each vector having the data concatenated with the stroke value

'''

import pandas as pd
import numpy as np
#from sklearn.svm import SVC
#from scipy import interpolate
from sklearn import preprocessing  # for scale (centering and normalizing vectors)
import pickle
import cPickle
from scipy.interpolate import UnivariateSpline


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


        # build an output array large enough to hold the vectors for each stroke and the (unicode -> int) stroke value (1 elts)
#        output_array = np.zeros((num_strokes, (num_resamplings_2 + num_resamplings) * num_params + 1))
        output_array = np.zeros((num_strokes, (5 * num_resamplings) * num_params + 1))
        print output_array.size

        print filename
        print num_params
        print num_resamplings_2
        print

	for i in range(0, num_strokes):

                # how far?
                if (i % 100 == 0):
                        print float(i)/num_strokes
	
		X_matrix = np.zeros((num_params, num_resamplings * 5)) # the array to store in (using original data and 2 derivs, 2 integrals)

                # the array to store reshaped resampled vector in
		X_2_vector_scaled = np.zeros((num_params, num_resamplings_2)) 

                # the array to store the above 2 concatenated
#		concatenated_X_X_2 = np.zeros((num_params, num_resamplings_2 + num_resamplings)) 
		concatenated_X_X_2 = np.zeros((num_params, num_resamplings * 5)) # the array to store in (using original data and 2 derivs, 2 integrals)

		# for each parameter (accelX, accelY, ...)

                # map the unicode character to int
                curr_stroke_val = stroke_dict[data1[i][0]]
                                        
                #print(len(curr_stroke))
                #print(curr_stroke[0])
                #print(curr_stroke[1])

		curr_data = data1[i][1]

                # fix if too short for interpolation - pad current data with 3 zeros
                if(len(curr_data) <= 3):
                        curr_data = np.concatenate([curr_data, np.zeros((3,num_params))])

		time = np.arange(0, len(curr_data), 1) # the sample 'times' (0 to number of samples)
		time_new = np.arange(0, len(curr_data), float(len(curr_data))/num_resamplings) # the resampled time points

		for j in range(0, num_params): # iterate through parameters

			signal = curr_data[:,j] # one signal (accelx, etc.) to interpolate
			# interpolate the signal using a spline or so, so that arbitrary points can be used 
			# (~30 seems reasonable based on data, for example)
                        
			#tck = interpolate.splrep(time, signal, s=0)  # the interpolation represenation
                        tck = UnivariateSpline(time, signal, s=0)

			# sample the interpolation num_resamplings times to get values
                        # resampled_data = interpolate.splev(time_new, tck, der=0) # the resampled data
                        resampled_data = tck(time_new)

                        # scale data (center, norm)
                        resampled_data = preprocessing.scale(resampled_data)
                        
                        # first integral
                        tck.integral = tck.antiderivative()
                        resampled_data_integral = tck.integral(time_new)

                        # scale data (center, norm)
                        resampled_data_integral = preprocessing.scale(resampled_data_integral)

                        # 2nd integral
                        tck.integral_2 = tck.antiderivative(2)
                        resampled_data_integral_2 = tck.integral_2(time_new)

                        # scale data (center, norm)
                        resampled_data_integral_2 = preprocessing.scale(resampled_data_integral_2)

                        # first deriv
                        tck.deriv = tck.derivative()
                        resampled_data_deriv = tck.deriv(time_new)

                        # scale
                        resampled_data_deriv = preprocessing.scale(resampled_data_deriv)

                        # second deriv
                        tck.deriv_2 = tck.derivative(2)
                        resampled_data_deriv_2 = tck.deriv_2(time_new)

                        #scale
                        resampled_data_deriv_2 = preprocessing.scale(resampled_data_deriv_2)


                        # concatenate into one vector
                        concatenated_resampled_data = np.concatenate((resampled_data, 
                                                                      resampled_data_integral, 
                                                                      resampled_data_integral_2, 
                                                                      resampled_data_deriv, 
                                                                      resampled_data_deriv_2))
                        
                        # store for the correct parameter, to be used later as part of inputs to SVM
 			X_matrix[j] = concatenated_resampled_data

			# while we're at it, square vector of resampled data to get a matrix, vectorize the matrix, and store
			#  for each X in list, multiply X by itself -> X_2
			#- vectorize X^2 (e.g. 10 x 10 -> 100 dimensions)
#			X_2_matrix = np.outer(concatenated_resampled_data, concatenated_resampled_data) # temp matrix for outer product
#			X_2_vector = np.reshape(X_2_matrix, -1) # reshape into a vector

			#- center and normalize X^2 by mean and standard deviation
#			X_2_vector_scaled[j] = preprocessing.scale(X_2_vector) 

			#- concatenate with input X -> 110 dimensions
#			concatenated_X_X_2[j] = np.concatenate([X_matrix[j], X_2_vector_scaled[j]])

# FOR NOW, ONLY USE X, NOT OUTER PRODUCT
			concatenated_X_X_2[j] = X_matrix[j]

                # NOTE, THIS SHOULD REALLY JUST BE A BIG VECTOR FOR EACH STROKE, SO RESHAPE BEFORE ADDING TO OUTPUT LIST
                # ALSO, THE STROKE VALUE SHOULD BE ADDED
                this_sample = np.concatenate((np.reshape(concatenated_X_X_2, -1), np.array([curr_stroke_val])))
                concatenated_samples = np.reshape(this_sample, -1)

                # ADD TO OUTPUT ARRAY
                output_array[i] = concatenated_samples
        
        print(output_array.size)
        
	return(output_array)


