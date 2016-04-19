# read in data for each stroke
# classify using all data 
# also use total time

# see how accurate

import pickle
#import cPickle
import matplotlib.pyplot as plt
import numpy as np
# from mpl_toolkits.mplot3d.axes3d import Axes3D

filename = "../data/MarieTherese_jul31_and_Aug07_all.pkl"
#filename = "data.pkl"
pkl_file = open(filename, 'rb')
data1 = pickle.load(pkl_file)

#print(data1)

# List[i][0] is the label of the ith stroke, 
#   while List[i][1] is the raw data matrix of the ith stroke.
#
# In the raw data part, it is a n by 16 matrix, 
#    every column out of the total 16 columns represent the data
#    from a sensor:
# column 0-2: acceleration of x, y, z axis
# column 3-5: gyroscope of x, y, z axis
# column 6-8: magnetic field detector of x, y, z axis
# column 9-12 are quaternions
# column 13-15 are euler angles.

# get all the unique labels

# for each label, keep track of how long each stroke is.
# dictionary containing numpy array for each stroke label

max_stroke_len = 0
stroke_labels_list = []
for i in range(0,len(data1)):
    # the stroke's data
    stroke_label = data1[i][0]
    stroke_labels_list.append(str(stroke_label))
    stroke_data = data1[i][1]
    stroke_length = len(stroke_data)
    if (stroke_length > max_stroke_len):
        max_stroke_len = stroke_length

#print(stroke_labels_list)

# make a dictionary of lists from     
stroke_labels_set = set(stroke_labels_list)
stroke_stats = dict.fromkeys(stroke_labels_set)
for key in stroke_labels_set:
    stroke_stats[key] = np.zeros(max_stroke_len + 1)

#print stroke_stats

for i in range(0,len(data1)):
    # the stroke's data
    stroke_label = str(data1[i][0])
    stroke_data = data1[i][1]
    stroke_length = len(stroke_data)

    # get the counts, increment
    length_counts = stroke_stats[stroke_label]
#    print stroke_label
#    print length_counts
    length_counts[stroke_length] = length_counts[stroke_length] + 1

    # update the stat 
    stroke_stats[stroke_label] = length_counts

print stroke_stats

# plot a histogram of lengths for each label 
import matplotlib.pyplot as plt

# for each key, plot a histogram of counts

for key in stroke_labels_set:
#plt.hist(gaussian_numbers)
    print (key)
    print(stroke_stats[key])
    plt.plot(stroke_stats[key])#, bins=20, histtype='step')
    plt.title("Stroke length counts")
    plt.xlabel(key)
    plt.ylabel("Frequency")
    plt.legend()  # add a legend

plt.show()



#  now plot the total and normalized vectors for each sensor

#  for each label
#  store the total and normalized total in a nparray in a dictionary
stroke_total_dict = dict.fromkeys(stroke_labels_set)
stroke_normd_total_dict = dict.fromkeys(stroke_labels_set)
for key in stroke_labels_set:
    stroke_total_dict[key] = np.zeros(16)
    stroke_normd_total_dict[key] = np.zeros(16)


for i in range(0,len(data1)):
    # the stroke's data
    stroke_label = data1[i][0]
    stroke_data = data1[i][1]
    print data1[i][0]
    print stroke_label

#     # acceleration
#     # slice to get the acceleration coordinates
    acc_X = stroke_data[:,0]
    acc_Y = stroke_data[:,1]
    acc_Z = stroke_data[:,2]

    



#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     ax.scatter(acc_X, acc_Y, acc_Z)

#     ax.set_title("Acceleration, stroke " + str(stroke_label) + " " + str(i))
#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')

# #    plt.show()
#     filename = "figs/Acceleration_stroke_" + str(stroke_label) + " " + str(i)
#     fig.savefig(filename + ".pdf")
#     plt.close(fig)

#     #################################
#     # gyroscope
#     # slice to get the gyroscope coordinates
#     gyr_X = stroke_data[:,3]
#     gyr_Y = stroke_data[:,4]
#     gyr_Z = stroke_data[:,5]

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     ax.scatter(gyr_X, gyr_Y, gyr_Z)

#     ax.set_title("Gyroscope, stroke " + str(stroke_label) + " " + str(i))
#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')

# #    plt.show()
#     filename = "figs/Gyroscope_stroke_" + str(stroke_label) + " " + str(i)
#     fig.savefig(filename + ".pdf")
#     plt.close(fig)

#     #################################
#     # magnetic sensor
#     # slice to get the magnetic coordinates
#     mag_X = stroke_data[:,6]
#     mag_Y = stroke_data[:,7]
#     mag_Z = stroke_data[:,8]

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     ax.scatter(mag_X, mag_Y, mag_Z)

#     ax.set_title("Magnetic, stroke " + str(stroke_label) + " " + str(i))
#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')

# #    plt.show()
#     filename = "figs/Magnetic_stroke_" + str(stroke_label) + " " + str(i)
#     fig.savefig(filename + ".pdf")
#     plt.close(fig)


#     #################################
#     # quaternion sensor
#     # slice to get the quaternion coordinates
#     quaternion_1 = stroke_data[:,9]
#     quaternion_2 = stroke_data[:,10]
#     quaternion_3 = stroke_data[:,11]
#     quaternion_4 = stroke_data[:,12]

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     ax.scatter(quaternion_1, quaternion_2, quaternion_3)

#     ax.set_title("Quaternion, stroke " + str(stroke_label) + " " + str(i))
#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')

# #    plt.show()
#     filename = "figs/Quaternion_stroke_" + str(stroke_label) + " " + str(i)
#     fig.savefig(filename + ".pdf")
#     plt.close(fig)

#    #################################

#     # euler sensor
#     # slice to get the euler coordinates
#     euler_X = stroke_data[:,13]
#     euler_Y = stroke_data[:,14]
#     euler_Z = stroke_data[:,15]

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     ax.scatter(euler_X, euler_Y, euler_Z)

#     ax.set_title("Euler, stroke " + str(stroke_label) + " " + str(i))
#     ax.set_xlabel('X Label')
#     ax.set_ylabel('Y Label')
#     ax.set_zlabel('Z Label')
