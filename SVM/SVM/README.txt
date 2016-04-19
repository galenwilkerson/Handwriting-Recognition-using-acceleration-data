
Run in this order:

- python2.7 test_preprocess.py
- python2.7 SVM.py
- python2.7 check_predictions.py

similarly for "linear" SVM (does not compute outer product of input vector)


Note that num_resamplings parameter of preprocess_data function determines how many times to sample from the interpolated spline.

-----------

Algorithm:

- read data for each stroke:
	- for each of the 16 parameters (accelx, accely, etc.), find the cubic spline that best fits the data.
	- re-sample from the spline <num_resamplings> times (10 or 20 is reasonable, since the mean number of samples per stroke is ~25)
	- reshape all of this into a vector -> X
	- compute the outer product of X * X -> X_2
	- rescale both X and X_2 (center and norm by standard deviation)
	- concatenate X and X_2 to form the input vector for the SVM
- train/test (many-fold)
- train the SVM model using 90% of the strokes
- test using the remaining 10% 

-----------

Preliminary results:  (not randomized many-fold testing)

- using 10 resamplings WITH outer product (X_2)	: 84%  accuracy
- using 20 resamplings  "      "    "    	: 81.6%

- using 10 resamplings WITHOUT     "    "    	: 76.7% 
- using 20 resamplings  "      "    "    	: 80% 

- using 10 resamples, only taking 2 derivatives, 2 integrals: 77% accuracy
- using 20 resamples, "           "               "  	    : 79.67%

- using 20 resamples, only using 2 derivatives  : 0.738709677419


NEED TO TRY ON LARGER DATASET, AND RANDOMIZE TESTING!
