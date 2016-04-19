## Begin to understand system dynamics

## load non-segmented data
#
## scale (center, normalize by variance)
#
## plot using ggplot over time

rm(list = ls())

library(ggplot2)


infilename <- "../data/nonsegmented_Rollschuhe_1_pen.csv"
pen.data = read.csv(infilename, header = TRUE, sep = ",")



## dat <- pen.data$acc_x
## mat <- data.matrix(dat)

## avg <- mean(dat)
## variance <- var(dat)

## centered_dat <- dat - avg
## scaled_dat <- centered_dat / variance



df_no_time <- data.frame(pen.data)





# here centers and divides by variance (same as sklearn's scale() )
#scaled <- scale(df_no_time, center = TRUE, scale = TRUE)
variance <- apply(df_no_time, 2, var)
scaled <- scale(df_no_time, center = TRUE, scale = variance)

scaled_dat <- data.frame(scaled)

#add an auto-id time column
time <- as.numeric(row.names(scaled_dat))
scaled_with_time <- data.frame(time, scaled_dat)


# plot
require(reshape)

df <- melt(scaled_with_time,  id = 'time', variable_name = 'series')
#df <- melt(scaled_mat, variable_name = 'series')

# plot on same grid, each series colored differently -- 
# good if the series have same scale
ggplot(df, aes(time,value)) + geom_line(aes(colour = series))
#   + scale_colour_brewer(palette="Spectral")


ggsave("scaled_variables_vs_time.pdf")
