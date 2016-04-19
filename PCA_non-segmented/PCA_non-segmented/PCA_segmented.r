# plot PCA information for each stroke

# load segmented data
# separate into unique strokes

# plot PCA


rm(list = ls())

require(graphics)

infilename <-  "../data/segmented_data.Rdata"
#pen.data = read.csv(infilename, header = FALSE, sep = ",")
load(infilename)
# concatenate into unique strokes




## The variances of the variables in the
## USArrests data vary by orders of magnitude, so scaling is appropriate
#(pc.cr <- princomp(pen.data))  # inappropriate
#princomp(USArrests, cor = TRUE) # =^= prcomp(USArrests, scale=TRUE)
## Similar, but different:
## The standard deviations differ by a factor of sqrt(49/50)

print(summary(pc.cr <- princomp(pen.data, cor = TRUE)))

print(loadings(pc.cr))  # note that blank entries are small but not zero
## The signs of the columns are arbitrary

fig.dir = "fig/"
name = "PCA_Rollschuhe_1"

####

title.name <- paste0("Screeplot:_", name)
file.name <- paste0(fig.dir,title.name,".pdf")
    
pdf(file.name)
plot(pc.cr) # shows a screeplot.
dev.off()

#####

title.name <- paste0("Biplot:_", name)
file.name <- paste0(fig.dir,title.name,".pdf")
    
pdf(file.name)
biplot(pc.cr)
dev.off()





