# Handwriting Recognition using Machine Learning and Signal Processing 

This was for a paid project (so data cannot be published) to use data from an inertial measurement unit (IMU) as an input source for handwriting recognition.

That is, the device would generate acceleration and magnetic signals, which could then be classified using machine learning techniques, to try to predict characters that were written.

With a new project and new data, it is best to take some time to: 

- Understand the data (really), and not just "throw" it into a machine learning toolbox.  This means visualization and "slicing and dicing" the data in many ways.  Histograms, time series, amount of bad or missing data, and data characteristics should be well-understood.  (for example, the frequency at which it was collected, how exactly it was it collected, was it pre-processed, etc. etc.)
- Think about the _process_ that generated the data.  In this case, it was the motion of a human hand on a flat surface, which has various implications:  
  - Data is basically from a continuous process (no teleportation)
  - A lot of the data is collected in a plane, and 3-dimensional 'events' might have some meaning
  - Motions were the result of the human hand having certain degrees of freedom and dynamics.
  - Motions represent user attempts to write a meaningful message in letters in a particular language.
    - Characters are an assembly of curved lines written over time.
    - Characters have a start and end, during which the pen has to be picked up off the surface.
  - Users might not be perfect at that language, etc. etc.

These folders contain many experiments on the data to understand it, including statistics, visualization, and classification, trying out various features to check how they improve classification accuracy.

Python and R languages were used, as well as signal processing and machine learning libraries (scikit learn).


