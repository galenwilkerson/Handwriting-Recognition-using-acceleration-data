#  determine the lags between two strokes with same label
rm(list = ls())

infilename <- "../data/segmented_flat.Rdata"

load(infilename)

strokes <- subset(pen.data, label == "e")

stroke_list <- split(strokes, strokes$Stroke_ID)


x1 <- subset(pen.data, Stroke_ID == 3)
x2 <- subset(pen.data, Stroke_ID == 6)

x1 <- x1[-1:-3,]


param_names <- names(x1[-3:-1])

for (param_name in param_names) {

    pdf(paste0("figs/",param_name, "_ccf.pdf"))
    ccf(x1[[param_name]], x2[[param_name]])
    dev.off()
}
