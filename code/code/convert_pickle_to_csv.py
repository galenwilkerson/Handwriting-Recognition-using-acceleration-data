# read in data for each stroke
# classify using all data 
# also use total time

# see how accurate

import numpy as np
import pickle
import cPickle
import csv
# from mpl_toolkits.mplot3d.axes3d import Axes3D

filename = "../data/MarieTherese_jul31_and_Aug07_all.pkl"
pkl_file = open(filename, 'rb')
data1 = cPickle.load(pkl_file)

num_params = len(data1[0][1][0])
num_strokes = len(data1)

# empty array to store final data, including label and absolute ID number
new_data = np.zeros((1,num_params + 2))

#for i in range(0,num_strokes):
i = 0
    
stroke_number = i

# the stroke's data
stroke_label = str(data1[i][0])
stroke_data = data1[i][1]


# grab the raw data array, add a column with the label and absolute stroke number (unique for each stroke, just in increasing order)
stroke_number_vector = np.array([np.repeat(stroke_number, len(stroke_data))])
label_vector = np.array([np.repeat(stroke_label,  len(stroke_data))])

print(stroke_number_vector.T.shape)
print(label_vector.T.shape)
print(stroke_data.shape)

#print(stroke_number_vector.T)
#print(label_vector.T)
#print(stroke_data)



new_entry = np.concatenate((stroke_number_vector.T, label_vector.T, stroke_data), axis=1)

    new_data = np.concatenate((new_data, new_entry), axis = 0)


# write the newly formatted data to .csv as a flat file
with open('../data/stroke_data_flat.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(0,len(new_data)):
        spamwriter.writerow(new_data[i])


