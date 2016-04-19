
use the wavelet transform modulus values to classify signal 
(classifying labels only, no segmentation here)

for each stroke
take the wavelet transform

based on stroke_length statistics (see plots from "marie" data),
use the componets between 2^1 and 2^6 
to build SVM input vector

resample from these scales  (edge effects??)








