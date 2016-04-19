'''
load one stroke

use best GMM from BIC optimization

label the phases of the stroke using the "best GMM"

color the time series for this stroke

plot the time series

'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.colors as c
from sklearn import mixture
import pandas as pd
import pickle

infile_name = "../data/segmented_flat.csv"
#infile_name = "../data/nonsegmented_Rollschuhe_1_pen.csv"
print("Reading data...")
data = pd.read_csv(infile_name)

# get stroke data
data_stroke = data[data['Stroke_ID'] == 3094]
stroke_values = np.array(data_stroke.values[:,3:9], dtype = float)

label = set(data_stroke.label).pop()

# load appropriate GMM (from best GMMs, chosen with BIC)
# has been fitted on larger data set
gmm_filename = "./best_GMMs/" + label + "_best_GMM.pkl"
gmm_file = open(gmm_filename, 'rb')
best_gmm = pickle.load(gmm_file)

# get two cols for proxy training and cluster plotting
X_train = stroke_values#[:,:2]

# concatenate the two datasets into the final training set
#X_train = np.vstack([shifted_gaussian, shifted_gaussian2, stretched_gaussian])

# fit a Gaussian Mixture Model with two components
#clf = mixture.GMM(n_components=15, covariance_type='full')
#clf.fit(X_train)
#clf = gmm

#stroke_phases = clf.predict(X_train)

# label the phases using a pre-trained (optimized) GMM 
stroke_phases_from_best = best_gmm.predict(X_train)

# add phase to data_stroke
data_stroke.insert(3, 'phase', stroke_phases_from_best)


# split by phase
# get list of phases for this stroke
phases_this_stroke = list(data_stroke.phase.unique())

phase_colors = dict()

#color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
color_list = ['b.', 'g.', 'r.', 'r.', 'c.', 'm.', 'y.', 'k.']

import matplotlib as mpl
import matplotlib.cm as cm

# convert phase ids to colors
norm = mpl.colors.Normalize(vmin=0, vmax=len(phases_this_stroke))
cmap = cm.hot
#cmap = cm.
#key = phases_this_stroke[0]
#x = float(key)/max(phases_this_stroke)


m = cm.ScalarMappable(norm=norm, cmap=cmap)
#print m.to_rgba(x)



i = 0
for p in phases_this_stroke:
    phase_colors[p] = color_list[i]
    i = i + 1

# parameters names
params = list(np.array(data_stroke.columns, dtype = 'string')[3:9])

this_label = "time series"

# for each parameter, plot time series, color it by phase
fig = plt.figure()

i = 0
for plot_pos in range(1,7):
    param = params[i]
    print(param)
    ax1 = fig.add_subplot(6,1,plot_pos)
    ax1.set_title(this_label + " " + param)

    for this_phase in phases_this_stroke:
        data_this_phase = data_stroke[data_stroke.phase == this_phase]
        #        print(phase_colors[this_phase])
        thisfrac = float(this_phase)/max(phases_this_stroke)
#        phase_color = cm.jet(norm(thisfrac))

        phase_color = m.to_rgba(thisfrac)
        
        print(phase_color)
        print(str(phase_color))
        print(this_phase)

      #  ax1.set_facecolor(phase_color)

        # plot this phase as a certain color

        # get first 6 parameters 
        #        params = list(np.array(data_this_phase.columns, dtype = 'string')[3:9])

        
        ax1.plot(data_this_phase.time, data_this_phase[param], color=phase_color, alpha = 0.5, hatch = '.')

#        ax1.plot(data_this_phase.time, data_this_phase[param], phase_colors[this_phase])

    i = i + 1

plt.tight_layout()
plt.show()

'''
# display predicted scores by the model as a contour plot
data_x = X_train[:,0]
data_y = X_train[:,1]

x = np.linspace(np.min(data_x), np.max(data_x))
y = np.linspace(np.min(data_y), np.max(data_y))
X, Y = np.meshgrid(x, y)
XX = np.array([X.ravel(), Y.ravel()]).T
Z = -clf.score_samples(XX)[0]
Z = Z.reshape(X.shape)


CS = plt.contour(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=1000.0),
                 levels=np.logspace(0, 3, 10))
CB = plt.colorbar(CS, shrink=0.8, extend='both')
plt.scatter(data_x, data_y, .8)

plt.title('Negative log-likelihood predicted by a GMM')
plt.axis('tight')
plt.show()
'''
