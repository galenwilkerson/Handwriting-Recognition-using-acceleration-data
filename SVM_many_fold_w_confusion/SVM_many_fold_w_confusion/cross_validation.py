'''
- load the preprocessed data, 
                # - preprocess, extract the features,
- construct training, testing sets
- pass into SVM
- generate accuracy, confusion metrics
'''

from sklearn import svm, datasets
import sklearn.cross_validation
from sklearn.metrics import confusion_matrix
import cPickle

import matplotlib.pyplot as plt

# import some data to play with
preprocessed_data_filename = "../data/preprocessed_data.pkl"
infile = open(preprocessed_data_filename,'rb')
input_data = cPickle.load(infile)

last_elt = input_data.shape[1] - 1
data = input_data[:,:last_elt]
targets = input_data[:,last_elt]

# Split the data into a training set and a test set
#X_train, X_test, y_train, y_test = train_test_split(data, targets, random_state=0)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, targets, test_size=0.4, random_state=0)

X_train.shape, y_train.shape

X_test.shape, y_test.shape

clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
print("clf score " + str(clf.score(X_test, y_test)))



##### 5 - fold cross-validation  ##############

clf = svm.SVC(kernel='linear', C=1)

scores = cross_validation.cross_val_score(clf, data, targets, cv=5)

print("5-fold cross-validation scores: " + str(scores))

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
