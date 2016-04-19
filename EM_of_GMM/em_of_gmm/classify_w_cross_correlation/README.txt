Use simple cross-correlation to classify strokes.

---------------------------------------------------------------------------------------------

Algorithm (1-dimensional for 1 parameter (accel_x, etc.)):

Training:

- load labeled stroke training data

- for each unique label L

	- for each stroke instance of label

		- align using cross-correlation

	- create model stroke M_L using average of aligned signals

- save model strokes M_L

-----------

Prediction / classification:

- load unknown/test data

- for each unknown stroke U

	- for each model stroke M_L

		- find cross-correlation of M_L with U -> store score in array

		- classify U as L with highest cross-correlation

- save predictions

---------------------------------------------------------------------------------------------

Algorithm (P-dimensional - for all parameters (accel_x, accel_y, etc.))

Training:

- load labeled stroke training data

- for each unique label L

	- for each parameter P	
	
		- for each stroke instance of label

			- align using cross-correlation

		- create model stroke M_L,P using average of aligned signals

- save model strokes M_L,P

-----------

Prediction / classification:

- load unknown/test data

- for each unknown stroke U

	- for each model stroke M_L,P

		- find cross-correlation of U with M_L,P -> store score in array

		- classify U as L having most max cross-correlations

- save predictions
