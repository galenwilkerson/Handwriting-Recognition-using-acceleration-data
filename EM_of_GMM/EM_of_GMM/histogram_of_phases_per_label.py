'''
load strokes for each label

classify using GMM for all strokes

plot histogram for each stroke
'''

# fixes plotting problem if no DISPLAY
#import matplotlib
#matplotlib.use('Agg')

import pickle
import matplotlib.colors
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab


def plot_hist(x, in_x_label, in_y_label, in_title):
    print(x)
    print(in_x_label)
    print(in_y_label)
    print(in_title)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # the histogram of the data
    n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
    ax.set_xlabel(in_x_label)
    ax.set_ylabel(in_y_label)
    ax.set_title(in_title)
    #    ax.set_ylim(0, 0.03)
    ax.grid(True)
    #plt.show()
    plt.savefig("figs/" + in_title + ".pdf")


f = open("best_GMMs/all_strokes_best_GMM.pkl", 'rb')
best_GMM = pickle.load(f)

# just use all the labeled colors, should be enough
phase_colors = matplotlib.colors.cnames.keys()#values()

# read all stroke data
infile_name = "../data/segmented_flat.csv"
print("Reading data...")
data = pd.read_csv(infile_name)

unique_labels = list(set(data['label']))
params = list(data.columns)[3:16]

for this_label in unique_labels:
    print("label: " + this_label)
    all_strokes_this_label = (data[data.label == this_label])
    values_this_label = np.array(all_strokes_this_label.values[:,3:9], dtype = float)
    # label the phases using a pre-trained (optimized) GMM 
    label_phases_from_best = best_GMM.predict(values_this_label)
    plot_hist(label_phases_from_best, "phase", "count", "phases_stroke_" + this_label)
    
    
