# load segmented data, plot stats:

# per unique stroke (e.g. all "e"s concatenated, etc.)
# stats to plot:
# min
# max
# mean
# median

#########################################################################
# load data

# for each parameter (accel_x, etc.)

#  for each unique stroke

#   plot the mean
#   plot the mean of every individual stroke
##########################################################################

rm(list = ls())
library(wavelets)
library(ggplot2)
#library(graphics)

infilename <- "../data/segmented_flat.Rdata"
load(infilename)

############### split by unique stroke label into data frames ################

list.of.strokes <- split(pen.data, pen.data$label)

fig.dir <- "./ggplot_figs/"

# the columns to use for statistics
params.to.plot = names(pen.data)[-1:-3]

for(param.to.plot in params.to.plot){

    stroke_means <- data.frame()
    stroke_vars <- data.frame()
    stroke_meds <- data.frame()
    stroke_mins <- data.frame()
    stroke_maxs <- data.frame()
    
    for (stroke in list.of.strokes) {

        stroke_name <- unique(stroke$label)
        avg <- mean(stroke[[param.to.plot]])
        v <- var(stroke[[param.to.plot]])
        med <- median(stroke[[param.to.plot]])
        min <- min(stroke[[param.to.plot]])
        max <- max(stroke[[param.to.plot]])

        stroke_means <- rbind(stroke_means, data.frame(stroke_name, avg))
        stroke_vars <- rbind(stroke_vars, data.frame(stroke_name, v))
        stroke_meds <- rbind(stroke_meds, data.frame(stroke_name, med))
        stroke_mins <- rbind(stroke_mins, data.frame(stroke_name, min))
        stroke_maxs <- rbind(stroke_maxs, data.frame(stroke_name, max))
        ## # for each subset by Stroke_ID, find the mean
        ## avgs <- mean(subset(stroke, Stroke_ID)[[param.to.plot]])

        ## ## now plot them all together, with the mean colored black
        ## ## would be nice to label key by number of samples in subgroup!
        ## title.name <- paste("Histogram:_", param.to.plot, sep="_")
        ## file.name <- paste0(fig.dir,title.name,".pdf")
        ## c <- ggplot(pen.data, aes(x = pen.data[[param.to.plot]], color = label)) +
        ##     geom_density() +
        ##         xlab(param.to.plot) +
        ##             ggtitle(title.name)
        
        ## ggsave(file.name, c)
        
    }

    ggplot(stroke_means, aes(x = stroke_name, y = avg)) +
        geom_point()
    ggsave(paste0("moments_figs/", param.to.plot,'means.pdf'))

    ggplot(stroke_vars, aes(x = stroke_name, y = v)) +
        geom_point()
    ggsave(paste0("moments_figs/", param.to.plot,'vars.pdf'))

    ggplot(stroke_meds, aes(x = stroke_name, y = med)) +
        geom_point()
    ggsave(paste0("moments_figs/", param.to.plot,'meds.pdf'))

    ggplot(stroke_mins, aes(x = stroke_name, y = min)) +
        geom_point()
    ggsave(paste0("moments_figs/", param.to.plot,'mins.pdf'))

    ggplot(stroke_maxs, aes(x = stroke_name, y = max)) +
        geom_point()
    ggsave(paste0("moments_figs/", param.to.plot,'maxs.pdf'))
}

rm(list = ls())
