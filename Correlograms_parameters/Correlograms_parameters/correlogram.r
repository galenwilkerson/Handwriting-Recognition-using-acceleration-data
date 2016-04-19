# read in unsegmented data
# plot the correlation between params. (accel_x, accel_y, etc.)

library(corrgram)

infilename <- "../data/nonsegmented_Rollschuhe_1_pen.csv"

pen.data = read.csv(infilename, header = TRUE, sep = ",")


pdf("correlations_not_ordered.pdf")
corrgram(pen.data, order=FALSE, main="pen parameter correlation")
dev.off()

pdf("correlations_ordered.pdf")
corrgram(pen.data, order=TRUE, main="pen parameter correlation")
dev.off()

#corrgram(mtcars, order=TRUE, lower.panel=panel.shade,
#  upper.panel=panel.pie, text.panel=panel.txt,
#  main="Car Milage Data in PC2/PC1 Order")
