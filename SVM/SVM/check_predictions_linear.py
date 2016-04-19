''' 
load predictions

load actual test data

check
'''

import cPickle
infile = open("../data/predictions_linear.pkl", 'rb')
predictions = cPickle.load(infile)

test_file = open("../data/test_data_linear.pkl", 'rb')
test_data = cPickle.load(test_file)

#test_correct = test_data[:,320]
test_correct = test_data[:,len(test_data[0]) - 1]

num_correct = 0
for i in range(0, len(predictions)):
    if (predictions[i] == test_correct[i]):
        num_correct = num_correct + 1
        

print float(num_correct)/len(predictions)
