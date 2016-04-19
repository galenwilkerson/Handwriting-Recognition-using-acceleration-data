# read in data for each stroke
# classify using all data 
# also use total time

# see how accurate

import pickle
import cPickle
# from mpl_toolkits.mplot3d.axes3d import Axes3D

filename = "MarieTherese_jul31_and_Aug07_all.pkl"
pkl_file = open(filename, 'rb')
data1 = cPickle.load(pkl_file)

data2 = []
for i in range(0,len(data1)):

#    data2[len(data2):] = []

    # the stroke's data
    stroke_label = str(data1[i][0])
    stroke_data = data1[i][1]
    data2[len(data2):] = [stroke_label,stroke_data]

    

output = open('data.pkl', 'w')
pickle.dump(data2, output)
