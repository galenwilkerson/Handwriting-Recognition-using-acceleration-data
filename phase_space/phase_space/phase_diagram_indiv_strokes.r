## load segmented data
## for each parameter
##   for each unique stroke label ("uK1", etc)
##       plot all phase diagrams for different occurences of that label (each different color):
##       find the derivative:  d_param
##       plot(parameter, d_param)



rm(list = ls())

infilename <-  "../data/segmented_flat.Rdata"
load(infilename)

library(ggplot2)

param_names <- names(pen.data)[-3:-1]
for (param_name in param_names) {

    print(param_name)
    
    unique_labels <- unique(pen.data$label)
    for (unique_label in unique_labels) {

        print(unique_label)
        
        s = subset(pen.data, label == unique_label)
        stroke_list = split(s, s$Stroke_ID)

        ## for storing phase information for all strokes with same unique label
        merged_data <- data.frame()

        for (indiv_stroke in stroke_list){
            
            param <- indiv_stroke$accel_x
            d_param <- diff(param)
            param <- param[-1]
            
            variance <- var(param)
            param_scaled <- scale(param, center = TRUE, scale = variance)

            var_d <- var(d_param)
            d_param_scaled <- scale(d_param, center = TRUE, scale = var_d)

            

            Stroke_ID <- indiv_stroke$Stroke_ID[-1]
            ##    label <- indiv_stroke$label
            label <- rep(unique_label, length(param_scaled))
            merged_data <- rbind(merged_data, data.frame(Stroke_ID, label, param_scaled, d_param_scaled))
            
        }
        
        ggplot(merged_data, aes(x = param_scaled, y = d_param_scaled, color=Stroke_ID)) +
            geom_path() +
                ggtitle(paste(param_names, unique(label), sep= "_"))

        ggsave(paste("label_figs/", param_name, unique_label, "scaled_phase.pdf", sep="_"))

    }
}

