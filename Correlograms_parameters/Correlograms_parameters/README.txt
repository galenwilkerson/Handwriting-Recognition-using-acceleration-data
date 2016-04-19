Read in the data (segmented, perhaps vs. unsegmented)

- plot a correlogram for each unique stroke.   (i.e. all "u"s, etc.) 
- we actually want to know the variance as well, so want to plot that somehow!



NOW, FOR EACH UNIQUE STROKE:

subset by stroke label -> data frame

for each stroke label, plot the correlation matrix

to compare strokes, perhaps PCA is more useful:

for each unique stroke:
   - concatenate all of the unique stroke data 
   - run pca, generate scree plot
   - put all plots in a matrix



