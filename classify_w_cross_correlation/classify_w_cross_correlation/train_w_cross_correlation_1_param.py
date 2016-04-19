'''
Algorithm (1-dimensional for 1 parameter (accel_x, etc.)):

Training:

- load labeled stroke training data, save both

- for each unique label L

        - get first stroke of label L

	- for each following stroke instance of label L

		- align with first stroke using cross-correlation

	- create model stroke M_L using average of aligned signals

- save model strokes M_L

run as:
python -u <thisfile>.py >& out &

needs figs/ folder
'''

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt
import csv

training_file_name = "../data/segmented_flat.csv"
sample_size = 10
dx = 1 # set to one, for shifting

print("reading data...")

data = pd.read_csv(training_file_name)
unique_labels = list(set(data['label']))
params = list(data.columns)[3:16]

print("labels are: " + str(unique_labels))

param = "accel_x"

outfilename = param + " model_strokes.csv"
outfile = file(outfilename, 'w')
csv_writer = csv.writer(outfile)

# for each unique label
#this_label = 'e'
for this_label in unique_labels:

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    print("processing label " + this_label)

    this_label_strokes = data[data['label'] == this_label]
    this_label_stroke_ids = set(this_label_strokes['Stroke_ID'])

    # get a list of strokes with that label
    all_strokes_this_label = []
    for stroke_id in this_label_stroke_ids:
        all_strokes_this_label.append(this_label_strokes[this_label_strokes['Stroke_ID'] == stroke_id])

    num_strokes = len(all_strokes_this_label)
    print(str(num_strokes) + " strokes with label " + this_label)

    # get first stroke
    first_stroke = all_strokes_this_label[0]

    # iterate through remaining strokes
    # lists to hold signals and their times
    signal_list = list([np.array(first_stroke[param])])
    time_list = list([np.array(first_stroke.time)])
    
    # for padding
    min_time = np.min(first_stroke.time) 
    max_time = np.max(first_stroke.time) 

    #for target_index in range(1, 2):
    for target_index in range(1, len(all_strokes_this_label)):

        target = all_strokes_this_label[target_index]
        shift = (np.argmax(signal.correlate(first_stroke[param], target[param])) - len(target[param])) * dx

        # adjust the target time
        new_time = np.array(target.time + shift)
        new_signal = np.array(target[param])

        # get the min, max time for padding
        if (np.min(new_time) < min_time):
            min_time = np.min(new_time)
        if (np.max(new_time) > max_time):
            max_time = np.max(new_time)

        # keep time and target signal
        signal_list.append(new_signal)
        time_list.append(new_time)

    whole_time_range = np.array(range(min_time, max_time + 1))

    # pad signals according to their time range, add to matrix for finding mean signal
    # THEIR MUST BE AN EASIER WAY!
    signal_matrix = np.array([np.zeros(len(whole_time_range))])
    for i in range(0, len(signal_list)):
    
        this_time = time_list[i]
        this_signal = signal_list[i]

        new_sig = this_signal

        # pad signal according to time range
        if(min_time < min(this_time)):
            left_pad = min(this_time) - min_time
            new_sig = np.lib.pad(new_sig, (left_pad,0), 'constant', constant_values=(0))
                             
        if(max(this_time) < max_time):
            right_pad = max_time - max(this_time)
            new_sig = np.lib.pad(new_sig, (0,right_pad), 'constant', constant_values=(0))

        signal_matrix = np.concatenate((signal_matrix, [new_sig]), axis = 0)

        ax1.plot(whole_time_range, new_sig, 'b-')


    # remove first row of zeros
    signal_matrix = signal_matrix[1:]

    # average strokes together to create model stroke
    mean_signal = np.mean(signal_matrix, axis = 0)

    # add label and parameter
    model_signal = mean_signal.tolist()
    model_signal.insert(0, param)
    model_signal.insert(0, this_label)

    whole_time_range_list = whole_time_range.tolist()
    whole_time_range_list.insert(0, param)
    whole_time_range_list.insert(0, this_label)

    print("saving, plotting...")

    # write out this stroke information
    model_stroke = [whole_time_range_list, model_signal]
    for row in model_stroke:
        csv_writer.writerow(row)


    # plot the mean, save fig
    ax1.plot(whole_time_range, mean_signal, 'k-')
    ax1.set_title(this_label + " " + param)
    fig.savefig("figs/" + this_label + "_" + param + ".pdf")
    plt.close(fig)

    print("done!")

    
