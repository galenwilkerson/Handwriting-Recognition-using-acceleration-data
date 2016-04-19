# load segmented data, plot stats:
#    - per individual stroke
#    - per unique stroke (e.g. all "e"s concatenated, etc.)

# stats to plot:
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

#data.dir <- "../data/"
infilename <- "../data/segmented_flat.csv"
pen.data = read.csv(infilename, header = TRUE, sep = ",")

#load(paste0(data.dir, infilename))


############### split by stroke into data frames ################

list.of.strokes <- split(pen.data, pen.data$Stroke_ID)

fig.dir <- "./fig/"

# remove first name, since is auto-id
#my.names = names(pen.data)[-1]
#my.names = names(pen.data)[-2]

# the columns to use for statistics
params.to.plot = names(pen.data)[-1:-3]

###########  ITERATE THROUGH STROKES ###############

for (stroke in list.of.strokes) {

############################ FOR EACH COLUMN (PARAMETER - ACCEL_X, ETC.) ###################################

    print(class(stroke))
    stroke.id <- stroke$Stroke_ID[1]
    label <- stroke$label[1]

    stroke.length <- length(stroke)
    
    for(param.to.plot in params.to.plot){

        print(param.to.plot)

        ## try ggplot with some smoothing of time series
        title.name <- paste("Time_Series:_", stroke.id, label, param.to.plot,  "len:", stroke.length, sep="_")
        file.name <- paste0(fig.dir,title.name,".pdf")
    
        c <- ggplot(pen.data, aes(time, pen.data[[param.to.plot]])) + aes(group = 1) + stat_smooth() + geom_point() +
            ggtitle(title.name)

        ggsave(c, file=file.name)
    
        ## # time series
        ## title.name <- paste0("Time Series:_", name)
        ## file.name <- paste0(fig.dir,title.name,".pdf")
        
        ## pdf(file.name)
        ## plot(pen.data[[param.to.plot]], main = title.name, type = "p", pch = ".")
        ## dev.off()
    
        ## histogram
        title.name <- paste("Histogram:_", stroke.id, label, param.to.plot,  "len:", stroke.length, sep="_")
        file.name <- paste0(fig.dir,title.name,".pdf")
        
        pdf(file.name)
        hist(pen.data[[param.to.plot]], breaks = 100, main = title.name)
        dev.off()
        
        ## auto-correlation
        title.name <- paste("Temporal_Autocorrelation:_", stroke.id, label, param.to.plot,  "len:", stroke.length, sep="_")
        file.name <- paste0(fig.dir,title.name,".pdf")

        pdf(file.name)
        acf(pen.data[[param.to.plot]], main = title.name)
        dev.off()
        
        ## wavelet transform
        title.name <- paste("Discrete_Wavelet_Transform:_", stroke.id, label, param.to.plot,  "len:", stroke.length, sep="_")
        file.name <- paste0(fig.dir,title.name,".pdf")
        
        pdf(file.name)
        temp.array <- as.numeric(pen.data[[param.to.plot]])
        dwt1 <- dwt(temp.array)
        plot(dwt1)
        title(title.name)
        dev.off()

        
        ## power spectral density
        title.name <- paste("Power_Spectral_Density:_", stroke.id, label, param.to.plot,  "len:", stroke.length, sep="_")
        file.name <- paste0(fig.dir,title.name,".pdf")

        pdf(file.name)
        spectrum(pen.data[[param.to.plot]], main = title.name)
        dev.off()
        
    }
}

rm(list = ls())
