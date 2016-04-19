'''
- take the second antiderivative of acceleration in X, Y, Z

- plot the path in 3D

- do they look like letters?
'''

# load data
# for each stroke
# fit a spline to the X, Y, Z acceleration
# draw it

import cPickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from scipy.interpolate import UnivariateSpline
import numpy as np

filename = "../data/MarieTherese_jul31_and_Aug07_all.pkl"
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

    #    print data1[i][0]


#     # acceleration
#     # slice to get the acceleration coordinates
    curr_data = data1[i][1]

    # fix if too short for interpolation - pad current data with 3 zeros
    if(len(curr_data) <= 3):
        curr_data = np.concatenate([curr_data, np.zeros((3,num_params))])

    time = np.arange(0, len(curr_data), 1) # the sample 'times' (0 to number of samples)

    acc_X = curr_data[:,0]
    acc_Y = curr_data[:,1]
    acc_Z = curr_data[:,2]

    # fit 2nd the antiderivative

    # the interpolation representation
    tck_X = UnivariateSpline(time, acc_X, s=0)

    # integrals
    tck_X.integral = tck_X.antiderivative()
    tck_X.integral_2 = tck_X.antiderivative(2)

    # the interpolation representation
    tck_Y = UnivariateSpline(time, acc_Y, s=0)

    # integrals
    tck_Y.integral = tck_Y.antiderivative()
    tck_Y.integral_2 = tck_Y.antiderivative(2)

    # the interpolation representation
    tck_Z = UnivariateSpline(time, acc_Z, s=0)

    # integrals
    tck_Z.integral = tck_Z.antiderivative()
    tck_Z.integral_2 = tck_Z.antiderivative(2)

    # plot 2nd integrals
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(tck_X.integral_2(time),tck_Y.integral_2(time),tck_Z.integral_2(time))

    ax.set_title("position, stroke " + str(stroke_label) + " " + str(i))
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

#    plt.show()
    filename = "../figs/position_stroke_" + str(stroke_label) + " " + str(i)
    fig.savefig(filename + ".pdf")
    plt.close(fig)


    # plot 1st integrals
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(tck_X.integral(time),tck_Y.integral(time),tck_Z.integral(time))

    ax.set_title("velocity, stroke " + str(stroke_label) + " " + str(i))
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

#    plt.show()
    filename = "../figs/velocity_stroke_" + str(stroke_label) + " " + str(i)
    fig.savefig(filename + ".pdf")
    plt.close(fig)
