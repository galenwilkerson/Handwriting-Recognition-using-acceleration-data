'''
load signals 

for each unique label, choose 5 at random

for now, just look at their gyr_z parameter

align signals using scipy cross correlation, 

plot the time series, save it with label name

run as:
python -u align.py >& out &

needs figs/ folder

'''
import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import pylab as plt

infile_name = "../data/segmented_flat.csv"
sample_size = 10

print("reading data...")

data = pd.read_csv(infile_name)
unique_labels = set(data['label'])
params = list(data.columns)[3:16]

print("labels are: " + str(unique_labels))

# for each unique label
for this_label in list(unique_labels):

    this_label_strokes = data[data['label'] == this_label]
    this_label_stroke_ids = set(this_label_strokes['Stroke_ID'])

    # get a list of strokes with that label
    all_strokes_this_label = []
    for stroke_id in this_label_stroke_ids:
        all_strokes_this_label.append(this_label_strokes[this_label_strokes['Stroke_ID'] == stroke_id])

    # get the list of strokes to plot
    # for each parameter
    #   add a subplot
    #   for each stroke
    #     find the shift from the first stroke
    #     plot it
    
    # choose 5 random strokes to sample
    num_strokes = len(all_strokes_this_label)
    print(str(num_strokes) + " strokes with label " + this_label)
    indices_to_sample = np.random.permutation(num_strokes)[0:sample_size].tolist()
    print("sampling " + str(sample_size) + " strokes " + str(indices_to_sample))


    # for each parameter
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.6, wspace=0.6)
    plot_pos = 1
    for param in params:

        #print(param)

        # get the first stroke
        first_stroke = all_strokes_this_label[indices_to_sample[0]]
        dx = 1 # for our signals, timestep is 1

        # plot it


        ax1 = fig.add_subplot(4,4,plot_pos)
        ax1.set_title(this_label + " " + param)
        ax1.plot(first_stroke.time, first_stroke[param], 'r-')

        for i in range(1, sample_size):

            target_index = indices_to_sample[i]
            #print(target_index)
            target = all_strokes_this_label[target_index]
            #    dx = np.mean(np.diff(first_stroke.time.values))
            shift = (np.argmax(signal.correlate(first_stroke[param], target[param])) - len(target[param])) * dx
            ax1.plot(target.time + shift, target[param], 'g-')

        plot_pos = plot_pos + 1
        #print(plot_pos)

        #    plt.show()
    print("saving plot")
    fig.savefig("figs/"+ this_label + ".pdf")


