'''
Load the best overall GMM

Create a global set of colors for these clusters

For each individual stroke, color the stroke using the best GMM

Overlay the time-series plots for all strokes.
'''

# fixes plotting problem if no DISPLAY
import matplotlib
matplotlib.use('Agg')

import pickle
import matplotlib.colors
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from joblib import Parallel, delayed


def plot_this_label(data, this_label):
    print("label: " + this_label)
    all_strokes_this_label = (data[data.label == this_label])
    values_this_label = np.array(all_strokes_this_label.values[:,3:9], dtype = float)
    # label the phases using a pre-trained (optimized) GMM 
    label_phases_from_best = best_GMM.predict(values_this_label)
    print("num phases this label: " + str(len(set(label_phases_from_best))))
    print("phases: ")
    print(set(label_phases_from_best))
    # add phase to data_stroke
    all_strokes_this_label.insert(3, 'phase', label_phases_from_best)

    stroke_ids = list(set(all_strokes_this_label.Stroke_ID))

    fig = plt.figure()

    #    for stroke_id in stroke_ids:
    #        print("Stroke id: " + str(stroke_id))
    #        stroke_data = all_strokes_this_label[all_strokes_this_label.Stroke_ID == stroke_id]
    i = 0
    for plot_pos in range(1,7):
        param = params[i]
        print("Parameter: " + param)
        ax1 = fig.add_subplot(3,2,plot_pos)
        ax1.set_title(this_label + " " + param)
        for this_phase in label_phases_from_best:
            # print(this_phase)
            #            data_this_phase = np.array(all_strokes_this_label[all_strokes_this_label.phase == this_phase].values[:,4:10], dtype=float)
            data_this_phase = all_strokes_this_label[all_strokes_this_label.phase == this_phase]
            #            stroke_phases_from_best = best_GMM.predict(data_this_phase)
            # add phase to all_strokes_this_label
            #            data_this_phase.insert(3, 'phase', stroke_phases_from_best)
            phase_color = phase_colors[this_phase]
            ax1.plot(data_this_phase.time, data_this_phase[param], color=phase_color, alpha = .5, linestyle = ".", marker = ".")
        i = i + 1

    plt.tight_layout()
    #    plt.show()
    print("saving...")
#    plt.savefig("figs/" + this_label + "_time_series.pdf")
    plt.savefig("figs/" + this_label + "_time_series.png")
    plt.close()




f = open("best_GMMs/all_strokes_best_GMM.pkl", 'rb')
best_GMM = pickle.load(f)

# just use all the labeled colors, should be enough
phase_colors = matplotlib.colors.cnames.keys()#values()

# read all stroke data
infile_name = "../data/segmented_flat.csv"
print("Reading data...")
data = pd.read_csv(infile_name)

unique_labels = list(set(data['label']))

# JUST FOR THIS TIME TO FINISH RUN
unique_labels = unique_labels[14:]


params = list(data.columns)[3:16]


# for each label
#  for each stroke
#   for each parameter
#    divide the stroke into its phases
#    for each phase
#     plot by color


#Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
Parallel(n_jobs=-1)(delayed(plot_this_label)(data, param) for param in params)

#for label in unique_labels:
#    plot_this_label(data, label)

