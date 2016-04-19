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
#infilename <- "../data/segmented_flat.csv"
infilename <- "../data/segmented_flat.Rdata"
#pen.data = read.csv(infilename, header = TRUE, sep = ",")

load(infilename)


############### split by unique stroke label into data frames ################

#list.of.strokes <- split(pen.data, pen.data$label)

fig.dir <- "./ggplot_figs/"

# remove first name, since is auto-id
#my.names = names(pen.data)[-1]
#my.names = names(pen.data)[-2]

# the columns to use for statistics
params.to.plot = names(pen.data)[-1:-3]
uniq.labels = unique(pen.data$label)

# plot acf for all unique values
acf_multiple<-function(l){
    
    df.temp<-df[df$a==l,]
    plot(df.temp$y,df.temp$z,xlab="Y Value",ylab="Z Value",
         main=paste("Value of key variable: ",toString(l)))
    abline(lm(df.temp$z~df.temp$y),col="red")
    
}

for(param.to.plot in params.to.plot){


    
    
    for(label in uniq.labels) {

        
        ## auto-correlation
        ## try also to plot multiple auto-correlations over each other
        ## create one acf per label
            
        title.name <- paste("Temporal_Autocorrelation:_", param.to.plot, sep="_")
        file.name <- paste0(fig.dir,title.name,".pdf")

        acf1 <- acf(pen.data[[param.to.plot]], plot = FALSE)
        c <-ggplot(data=subset(X, Year>1980)) + # ggplot() +
            geom_line(aes(x = acf1$lag, y = acf1$acf)) +
                ggtitle(title.name)
    }
    
    ggsave(file.name, c)
        
}

## ###########  ITERATE THROUGH STROKES ###############

## for (stroke in list.of.strokes) {

## ############################ FOR EACH COLUMN (PARAMETER - ACCEL_X, ETC.) ###################################

##     print(class(stroke))
##     #stroke.id <- stroke$Stroke_ID[1]
##     label <- stroke$label[1]

##     num.samples <- dim(stroke)[1]
##     print(num.samples)
    
##     for(param.to.plot in params.to.plot){

##         print(param.to.plot)

##         ################# or ggplot2
        
##         ## ## try ggplot with some smoothing of time series
##         ## title.name <- paste("Time_Series:_", label, param.to.plot,  "len:", num.samples, sep="_")
##         ## file.name <- paste0(fig.dir,title.name,".pdf")
    
##         ## c <- ggplot(pen.data, aes(time, pen.data[[param.to.plot]])) + aes(group = Stroke_ID) +
##         ##     stat_smooth() +
##         ##        # geom_point() +
##         ##        # geom_line() +
##         ##         ggtitle(title.name)

##         ## ggsave(c, file=file.name)

##         ################# or standard plot
        
##         ## # time series
##         ## title.name <- paste0("Time Series:_", name)
##         ## file.name <- paste0(fig.dir,title.name,".pdf")
        
##         ## pdf(file.name)
##         ## plot(pen.data[[param.to.plot]], main = title.name, type = "p", pch = ".")
##         ## dev.off()
    
##         ## histogram
##         title.name <- paste("Histogram:_", label, param.to.plot,  "len:", num.samples, sep="_")
##         file.name <- paste0(fig.dir,title.name,".pdf")
        
##         ## pdf(file.name)
##         ## hist(pen.data[[param.to.plot]], breaks = 100, main = title.name)
##         ## dev.off()

        
        
        
##         ## ## auto-correlation
##         ## title.name <- paste("Temporal_Autocorrelation:_", label, param.to.plot,  "len:", num.samples, sep="_")
##         ## file.name <- paste0(fig.dir,title.name,".pdf")

##         ## pdf(file.name)
##         ## acf(pen.data[[param.to.plot]], main = title.name)
##         ## dev.off()
        
##         ## ## wavelet transform
##         ## title.name <- paste("Discrete_Wavelet_Transform:_", label, param.to.plot,  "len:", num.samples, sep="_")
##         ## file.name <- paste0(fig.dir,title.name,".pdf")
        
##         ## pdf(file.name)
##         ## temp.array <- as.numeric(pen.data[[param.to.plot]])
##         ## dwt1 <- dwt(temp.array)
##         ## plot(dwt1)
##         ## title(title.name)
##         ## dev.off()

        
##         ## ## power spectral density
##         ## title.name <- paste("Power_Spectral_Density:_", label, param.to.plot,  "len:", num.samples, sep="_")
##         ## file.name <- paste0(fig.dir,title.name,".pdf")

##         ## pdf(file.name)
##         ## spectrum(pen.data[[param.to.plot]], main = title.name)
##         ## dev.off()
        
##     }
## }

rm(list = ls())
