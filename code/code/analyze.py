import cPickle
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d.axes3d import Axes3D

filename = "MarieTherese_jul31_and_Aug07_all.pkl"
pkl_file = open(filename, 'rb')
data1 = cPickle.load(pkl_file)

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

# for each stroke, plot the x,y coordinates of the accelerator, magnet, etc.

for i in range(0,len(data1)):
    # the stroke's data
    stroke_label = data1[i][0]
    stroke_data = data1[i][1]
    print data1[i][0]
    #print stroke_label

#     # acceleration
#     # slice to get the acceleration coordinates
#     acc_X = stroke_data[:,0]
#     acc_Y = stroke_data[:,1]
#     acc_Z = stroke_data[:,2]

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

# #    plt.show()
#     filename = "figs/Euler_stroke_" + str(stroke_label) + " " + str(i)
#     fig.savefig(filename + ".pdf")
#    plt.close(fig)
