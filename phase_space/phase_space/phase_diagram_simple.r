## load non-segmented data
## for each parameter
##    find the derivative:  d_param
##    plot(parameter, d_param)

rm(list = ls())


infilename <- "../data/nonsegmented_Rollschuhe_1_pen.csv"

pen.data = read.csv(infilename, header = TRUE, sep = ",")

library(ggplot2)


param_names <- names(pen.data)

for (param_name in param_names) {

    param <- pen.data[[param_name]]
    d_param <- diff(param)

    # remove first entry so vectors are same length (for plotting)
    param <- param[-1]
    
    # re-scale (center and norm by variance) both axes

    variance <- var(param)
    param_scaled <- scale(param, center = TRUE, scale = variance)

    
    var_d <- var(d_param)
    d_param_scaled <- scale(d_param, center = TRUE, scale = var_d)
    
#    qplot(param, d_param)
    qplot(param_scaled, d_param_scaled) + geom_path()

    ggsave(paste0("figs/", param_name , "_scaled_phase.pdf"))
}
