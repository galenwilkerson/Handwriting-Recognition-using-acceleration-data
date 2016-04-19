'''
want to see sub-clusters (phases) of each stroke
(think of each stroke as a cloud in high-dimensional space)
consider using only first 6 parameters

---
load strokes of one label

use BIC to determine best number of clusters for strokes of same label

color average stroke according to clusters
'''

# fix the DISPLAY
import matplotlib
matplotlib.use('Agg')


import itertools

import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn import mixture
import pandas as pd

import pickle

from joblib import Parallel, delayed


def find_best_GMM(X, n_components_range):
    lowest_bic = np.infty
    bic = []
    #n_components_range = range(1,21)
    cv_types = ['spherical', 'tied', 'diag', 'full']
    for cv_type in cv_types:
        print cv_type
        for n_components in n_components_range:
            print n_components
            # Fit a mixture of Gaussians with EM
            gmm = mixture.GMM(n_components=n_components, covariance_type=cv_type)
            gmm.fit(X)
            bic.append(gmm.bic(X))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
    return((best_gmm, lowest_bic, bic))

# save the figure
def plot_BIC(n_components_range, bic, best_gmm, label):

    bic = np.array(bic)
    cv_types = ['spherical', 'tied', 'diag', 'full']
    color_iter = itertools.cycle(['k', 'r', 'g', 'b', 'c', 'm', 'y'])
    clf = best_gmm
    bars = []

    # Plot the BIC scores
    spl = plt.subplot(1, 1, 1)
    for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
        xpos = np.array(n_components_range) + .2 * (i - 2)
        bars.append(plt.bar(xpos, bic[i * len(n_components_range):
                                      (i + 1) * len(n_components_range)],
                            width=.2, color=color))
    plt.xticks(n_components_range)
    plt.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
    plt.title(label + ' BIC score per model')
    xpos = np.mod(bic.argmin(), len(n_components_range)) + .65 +\
        .2 * np.floor(bic.argmin() / len(n_components_range))
    plt.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
    spl.set_xlabel('Number of components')
    spl.legend([b[0] for b in bars], cv_types)

    # save figure and best model
    plt.savefig("figs/" + label + "_BIC.pdf")

# find and plot the best GMM, save figure and results
def find_plot_GMM(data, n_components_range, label):
    print("Processing " + label)
    data_this_label = data[data['label'] == label]

    # ONLY USE ACCEL AND GYR PARAMETERS [3-9]
    X = np.array(data_this_label.values[:,3:9], dtype=float)

    # find the best GMM
    (best_gmm, lowest_bic, bic) = find_best_GMM(X, n_components_range)

    # plot the BIC values
    plot_BIC(n_components_range, bic, best_gmm, label)

    # save the best GMM model
    outfilename = "best_GMMs/" + label+"_best_GMM.pkl"
    f = open(outfilename, "wb")
    pickle.dump(best_gmm, f)
    f.close()

    return(best_gmm, lowest_bic)

infile_name = "../data/segmented_flat.csv"
print("Reading data...")
data = pd.read_csv(infile_name)

n_components_range = range(1,21)

labels = set(data['label'])
print(labels)

Parallel(n_jobs=-1, verbose=5)(delayed(find_plot_GMM)(data, n_components_range, label) for label in labels)

# find and plot the best GMM
#find_plot_GMM(data, n_components_range, label)

#print("Winner:")
#print(best_gmm)
#print("lowest BIC:")
#print(lowest_bic)


