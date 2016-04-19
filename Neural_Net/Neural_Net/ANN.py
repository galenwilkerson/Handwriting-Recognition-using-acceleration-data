''' 
- preprocess the data (or load preprocessed data)
- train the SVM
- test it
'''



def ANN(input_data):
    print(input_data.shape)

    # train the SVM
    model = SVC(kernel='linear')

    # test and training data
    data_size = len(input_data)
    training_size = int(.9 * data_size)
    test_size = data_size - training_size

    print(data_size)
    print(training_size)
    print(test_size)

    training_data = input_data[0:training_size]
    test_data = input_data[training_size:]

    # save training and test data
    training_data_file = open("../data/training_data.pkl", 'wb')
    cPickle.dump(training_data, training_data_file)
    test_data_file = open("../data/test_data.pkl", 'wb')
    cPickle.dump(test_data, test_data_file)


    # the size of the training vectors
    num_columns = len(training_data[0])



    # fit the model using the parameters and the stroke labels
    model = model.fit(training_data[:,0:(num_columns-1)],np.ravel(training_data[:,num_columns-1:]))
    #model = model.fit(training_data[:,0:(num_columns-1)],np.transpose(training_data[:,num_columns-1:]))
    #model = model.fit(np.transpose(training_data[:,0:(num_columns-1)]),np.transpose(training_data[:,num_columns-1:]))
    
    # test it
    output = model.predict(test_data[:,0:(num_columns-1)])
    predict_filename = "../data/predictions.pkl"
    predict_file = open(predict_filename, 'wb')
    cPickle.dump(output, predict_file)


import numpy as np
from sklearn.svm import SVC
#import preprocess
import cPickle

# load data
preprocessed_data_filename = "../data/preprocessed_data.pkl"
infile = open(preprocessed_data_filename,'rb')
input_data = cPickle.load(infile)

SVM(input_data)
