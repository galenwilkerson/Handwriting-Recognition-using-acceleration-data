''' 
- read in the preprocessed data
- train the SVM
- make some predictions
'''

import numpy as np
from sklearn import svm
#from sklearn.svm import SVC
#import preprocess
import cPickle
import csv
from sklearn import cross_validation

# load data
#preprocessed_data_filename = "../data/preprocessed_data.pkl"
#infile = open(preprocessed_data_filename,'rb')
#input_data = cPickle.load(infile)
#preprocessed_data_filename = "./preprocessed_data.csv"
preprocessed_data_filename = "./feature_vector.csv"
fin = open(preprocessed_data_filename, 'rt')# as fin: # context manager
cin = csv.reader(fin)
input_data = [row for row in cin]

#print(input_data.shape)

# convert each row to a row of an np.array
input_matrix = np.zeros([1,len(input_data[0])])

for entry in input_data:
    row_array = np.array([map(float, entry)])
    input_matrix = np.concatenate((input_matrix, row_array), axis=0)

# clean up the first row
input_matrix = np.delete(input_matrix, (0), axis=0)
input_data = input_matrix
del(input_matrix)

print("done loading, training SVM...")

data = input_data[:,:1281]
target = input_data[:,1281]

X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, target, test_size=0.9, random_state=0)

clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
print(clf.score(X_test, y_test))



# # train the SVM
# model = SVC(kernel='linear')

# # test and training data
# data_size = len(input_data)
# training_size = int(.9 * data_size)
# test_size = data_size - training_size

# print(data_size)
# print(training_size)
# print(test_size)

# training_data = input_data[0:training_size]
# test_data = input_data[training_size:]

# # save training and test data
# training_data_file = open("../data/training_data.pkl", 'wb')
# cPickle.dump(training_data, training_data_file)
# test_data_file = open("../data/test_data.pkl", 'wb')
# cPickle.dump(test_data, test_data_file)


# # the size of the training vectors
# num_columns = len(training_data[0])


# print("fitting ")


# # fit the model using the parameters and the stroke labels
# model = model.fit(training_data[:,0:(num_columns-1)],np.ravel(training_data[:,num_columns-1:]))
# #model = model.fit(training_data[:,0:(num_columns-1)],np.transpose(training_data[:,num_columns-1:]))
# #model = model.fit(np.transpose(training_data[:,0:(num_columns-1)]),np.transpose(training_data[:,num_columns-1:]))


# print("predicting")

# # test it
# output = model.predict(test_data[:,0:(num_columns-1)])
# predict_filename = "../data/predictions.pkl"
# predict_file = open(predict_filename, 'wb')
# cPickle.dump(output, predict_file)

# print("done!")
