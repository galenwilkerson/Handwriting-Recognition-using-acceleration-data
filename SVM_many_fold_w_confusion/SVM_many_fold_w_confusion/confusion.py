'''
- load the preprocessed data, 
                # - preprocess, extract the features,
- construct training, testing sets
- pass into SVM
- generate accuracy, confusion metrics
'''

from sklearn import svm, datasets
from sklearn.cross_validation import train_test_split
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
X_train, X_test, y_train, y_test = train_test_split(data, targets, random_state=0)

# Run classifier
classifier = svm.SVC(kernel='linear')
y_pred = classifier.fit(X_train, y_train).predict(X_test)



# Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)

print(cm)


# # load the label dictionary from file, for axis labels
# dict_filename = "../data/stroke_label_mapping.pkl"
# dict_file = open(dict_filename, 'rb')
# stroke_dict = pickle.load(dict_file)

# # reverse the dictionary (yes array would be better)
# for key in stroke_dict.iterkeys():
#     stroke_num_names[stroke_dict[key]] = key

# class_labels = stroke_num_names.values()



# Show confusion matrix in a separate window
plt.matshow(cm)
plt.title('Confusion matrix')
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
#plt.show()

filename = "figs/confusion_matrix.pdf"

plt.savefig(filename)
plt.close(fig)
