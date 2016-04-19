import os
import pickle

filenames = os.listdir("./best_GMMs/")


for filename in filenames:
    gmm = pickle.load(open("./best_GMMs/"+filename, 'rb'))
    print filename
    print gmm.covariance_type
    print gmm.n_components
    print
