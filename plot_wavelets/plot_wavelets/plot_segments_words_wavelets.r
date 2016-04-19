# load non-segmented data
# for each parameter, find WTMM

rm(list = ls())

require(graphics)
library(wmtsa)

# load(../data/nonsegmented_Rollschuhe_1_pen.csv")
#infilename <- "../data/nonsegmented_Rollschuhe_1_pen.csv"

# segmented, labeled, full data
infilename <- "../data/full_segmented_labeled_data/brownfox/brownfox_2014-09-25T13:26:57.057350_pen.csv"
#infilename <- "../data/full_segmented_labeled_data/brownfox/brownfox_2014-09-25T13:18:25.553282_pen.csv"

pen.data = read.csv(infilename, header = TRUE, sep = ",")


param.names <- names(pen.data)[-5:-1]
#param_name = "acc_x"

for (param_name in param.names) {

    y <- signalSeries(pen.data[[param_name]])
    ##y <- signalSeries(pen.data[[param_name]], pen.data$t_board)
    x <- 1:length(y)


    ## calculate CWT using Mexican hat filter
    wavelet_type = "gaussian1"
    ##wavelet_types = list("gaussian1", "gaussian2")
    
    ##for (wavelet_type in wavelet_types) {
    W <- wavCWT(y, wavelet=wavelet_type)

    plot(W, main = paste(param_name, wavelet_type))
    
    ## find when the pen state changes
    pen.change = diff(pen.data$press)
    pen.change = append(0, pen.change)

    pen.data$pen.change <- pen.change

    ##  now plot the beginning and end of each stroke
    new.press = subset(pen.data, pen.change == 1)
    stop.press = subset(pen.data, pen.change == -1)
    abline(v = rownames(new.press), lty = 3)
    abline(v = rownames(stop.press),lty = 3)

    mtext(new.press$label, 1, at = rownames(new.press))
}


## ## calculate WTMM and extract first two branches
## ## in tree corresponding to the cusps
## W.tree <- wavCWTTree(W, n.octave.min = .25)#[1:2]
    
## ## plot the CWT tree overlaid with a scaled
## ## version of the time series to illustrate
## ## alignment of branches with cusps
## yshift <- y@data - min(y@data)
## yshift <- yshift / max(yshift) * 4 - 4.5
## plot(W.tree, xlab="x", main = paste(param_name, wavelet_type))
## #    lines(x, yshift, lwd=2)
## text(6.5, -1, "f(x) = -0.2|x-1|^0.5 - 0.5|x-15|^0.3 + 0.00346x + 1.34", cex=0.8)

## ## estimate Holder exponents
## holder <- holderSpectrum(W.tree)
## print(wavelet_type)
## print(holder)
## #}


