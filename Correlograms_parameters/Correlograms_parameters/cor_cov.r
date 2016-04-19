# read in unsegmented data
# plot the correlation between params. (accel_x, accel_y, etc.)

library(lattice)

infilename <- "../data/nonsegmented_Rollschuhe_1_pen.csv"

pen.data = read.csv(infilename, header = TRUE, sep = ",")


# Correlations/covariances among numeric variables in
# data frame mtcars. Use listwise deletion of missing data.
#cor(mtcars, use="complete.obs", method="kendall")
#cov(mtcars, use="complete.obs")


co = cor(pen.data)
cv = cov(pen.data)


pdf("corr.pdf")
levelplot(co)
dev.off()


## pdf("covar.pdf")
## levelplot(cv)
## dev.off()

## pdf("log_covar.pdf")
## levelplot(log(cv))
## dev.off()


library(ggplot2)
library(reshape)

z <- cor(pen.data)
z.m <- melt(z)

ggplot(z.m, aes(X1, X2, fill = value)) + geom_tile() + 
    scale_fill_gradient(low = "black",  high = "white") +
        theme(axis.text.x = element_text(angle = 45, hjust = 1))
ggsave("corr_ggplot.pdf")
