import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn import mixture
import pandas as pd


'''
load one stroke

do basic GMM clustering

color the time series

'''

infile_name = "../data/nonsegmented_Rollschuhe_1_pen.csv"
print("Reading data...")
data = pd.read_csv(infile_name)
X_train = data.values[:,(4,5)]#[:,:2]

# concatenate the two datasets into the final training set
#X_train = np.vstack([shifted_gaussian, shifted_gaussian2, stretched_gaussian])

# fit a Gaussian Mixture Model with two components
clf = mixture.GMM(n_components=30, covariance_type='full')
clf.fit(X_train)


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
