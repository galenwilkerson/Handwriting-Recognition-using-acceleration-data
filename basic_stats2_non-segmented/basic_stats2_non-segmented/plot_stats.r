# load non-segmented data, plot stats

# plot:
# time series
# histogram of values,
# autocorrelation, and
# wavelet transform
# power spectral density (to understand noise)
# for each parameter (dimenion) - accelx, accely, etc.


#########################################################################
# load data

# for each parameter (accel_x, etc.)

   # compute histogram for each parameter
   # compute autocorrelation for each parameter
   # compute the wavelet transform for each dimension
   # save all figures


##########################################################################

rm(list = ls())
library(wavelets)
library(ggplot2)
#library(graphics)

# load(../data/nonsegmented_Rollschuhe_1_pen.csv")
infilename <- "../data/nonsegmented_Rollschuhe_1_pen.csv"

pen.data = read.csv(infilename, header = TRUE, sep = ",")

############################ FOR EACH COLUMN (PARAMETER - ACCEL_X, ETC.) ###################################

# add a "time" column, just auto-numbered
time <- rownames(pen.data)
pen.data <- cbind(time=time, pen.data)

fig.dir <- "./fig/"
# remove first name, since is auto-id
my.names = names(pen.data)[-1]

for(name in my.names){

    print(name)

    # try ggplot with some smoothing of time series
    title.name <- paste0("Time Series:_", name)
    file.name <- paste0(fig.dir,title.name,".pdf")
    
    c <- ggplot(pen.data, aes(time, pen.data[[name]])) + aes(group = 1) + stat_smooth() + geom_point() +
        ggtitle(title.name)

    ggsave(c, file=file.name)
    
    ## # time series
    ## title.name <- paste0("Time Series:_", name)
    ## file.name <- paste0(fig.dir,title.name,".pdf")
    
    ## pdf(file.name)
    ## plot(pen.data[[name]], main = title.name, type = "p", pch = ".")
    ## dev.off()

    
    # histogram
    title.name <- paste0("Histogram:_", name)
    file.name <- paste0(fig.dir,title.name,".pdf")
    
    pdf(file.name)
    hist(pen.data[[name]], breaks = 100, main = title.name)
    dev.off()
    
    # auto-correlation
    title.name <- paste0("Temporal_Autocorrelation:_", name)
    file.name <- paste0(fig.dir,title.name,".pdf")

    pdf(file.name)
    acf(pen.data[[name]], main = title.name)
    dev.off()
    
    
    # wavelet transform
    title.name <- paste0("Discrete_Wavelet_Transform:_", name)    
    file.name <- paste0(fig.dir,title.name,".pdf")
    
    pdf(file.name)
    temp.array <- as.numeric(pen.data[[name]])
    dwt1 <- dwt(temp.array)
    plot(dwt1)
    title(title.name)
    dev.off()

    
    # power spectral density
    title.name <- paste0("Power_Spectral_Density:_", name)    
    file.name <- paste0(fig.dir,title.name,".pdf")

    pdf(file.name)
    spectrum(pen.data[[name]], main = title.name)
    dev.off()
    
}
     
rm(list = ls())
