# Handwriting Recognition using Machine Learning and Signal Processing 

This was for a paid project (so data cannot be published) to use data from an inertial measurement unit (IMU) as an input source for handwriting recognition.

That is, the device would generate acceleration and magnetic signals, which could then be classified using machine learning techniques, to try to predict characters that were written.

With a new project and new data, it is best to take some time to: 

- Understand the data (really), and not just "throw" it into a machine learning toolbox.  This means visualization and "slicing and dicing" the data in many ways.  Histograms, time series, amount of bad or missing data, and data characteristics should be well-understood.  (for example, the frequency at which it was collected, how exactly it was it collected, was it pre-processed, etc. etc.)
- Think about the _process_ that generated the data.  In this case, it was the motion of a human hand on a flat surface, which has various implications:  
  - Data is basically from a continuous process (no teleportation)
  - A lot of the data is collected in a plane, and 3-dimensional 'events' might have some meaning
  - Motions were the result of the human hand having certain degrees of freedom and dynamics.
  - Motions represent user attempts to write a meaningful message in characters in a particular language.
    - Characters are an assembly of curved lines written over time.
    - Characters have a start and end, during which the pen has to be picked up off the surface.
  - Users might not be perfect at that language, be in different emotional states, or have other factors

These folders contain many experiments on the data to understand it, including statistics, visualization, and classification, trying out various features to check how they improve classification accuracy.

Some folders of interest:

- figs/ - what does the raw data look like? How many points in a character?  Are the points clustered?  
- PCA_per_stroke/  - if we look at all columns of data (there were several instruments collecting data simultaneously), which principle components seem to account for the most variation?
- align_signals/   - with two known characters, try to see if their signals can be time-lagged aligned using the scipy cross-correlation function
- SVM/   - with segmented, labeled data, try to:
  - extract features by resampling the signal with a spline over time duration of the entire character (since characters have different time duration)
  - center and norm the result and do "feature expansion" (take outer product of input data vector)
  - use this as input for training a Support Vector Machine
  - do many-fold testing and find accuracy
  - approximately 80% accuracy was obtained in the first 3 days of working on this project using this approach which I developed.
  
- Unfortunately, this was a startup company, so there was absolutely _no_time_ to do things properly.  However, other features were attempted (or just considered) with varying amounts of success, such as:
  - plot normalized cross correlation - For each pair (cross-product) of characters in the input data, the cross-correlation was calculated, then plotted in a heat-map, to try to understand if this would be a good feature to use for classification. 
  - wavelet transform of the input signals as a feature vector
  - considering the characters as a sequence of curves
  - stroke network - thinking of a each character as a node in a network and using characters' cross-correlation as the weight in the network, to see if characters were grouped together
  - and others!

Python and R languages were used, as well as signal processing and machine learning libraries (scikit learn).


