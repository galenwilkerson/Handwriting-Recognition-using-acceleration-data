
# load data

# subset by stroke (k1, e, etc.)

# find auto-correlation 

########################################################

rm(list = ls())
library(ggplot2)
library(scales)
library(wavelets)
library(xts)

########################################################


############################################################################



data.dir = "/home/username/Dropbox/Active_Projects/Mobility_Article/Data/"
figures.dir = "./Figures/"

load(paste(data.dir, "trips.Rdata", sep=""))

# get events within time range ########################################

## - from June 1 to Oct. 1, 2008

start.time <- as.POSIXlt("2008-06-01 00:00:00 CEST")
end.time <- as.POSIXlt("2008-10-01 00:00:00 CEST")
events.within.period <- subset.events.time.period(trips, time.column.name = "timestamp.event", start.time = start.time, end.time = end.time)


events <- events.within.period


## ## - on a weekday
## ## - between 9am and 2pm
## events.within.period$timestamp.event <- as.POSIXlt(events.within.period$timestamp.event)
## temp.events <- unclass(events.within.period$timestamp.event)
## temp.df <- data.frame(events.within.period, temp.events)
## events.on.day <- subset(temp.df, wday >= 1 & wday <= 5)

## events.in.range <- subset(events.on.day, hour >= 9 & hour <= 14)

## events <- events.in.range

############################## AUTOCORRELATION #############################

# make sure sorted in order of event
events <- events[order(events$timestamp.event),]

# bin by month
breaks.interval <- "month"

my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

print(length(my.table))

#  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

pdf(paste(figures.dir, "acf_", breaks.interval, "all_modes.pdf", sep=""))
acf(my.table, main=breaks.interval)
dev.off()

# bin by week
breaks.interval <- "week"

my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

print(length(my.table))

#  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

pdf(paste(figures.dir, "acf_", breaks.interval, "all_modes.pdf", sep=""))
acf(my.table, main=breaks.interval)
dev.off()


# bin by day
breaks.interval <- "day"

my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

print(length(my.table))

#  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

pdf(paste(figures.dir, "acf_", breaks.interval, "all_modes.pdf", sep=""))
acf(my.table, main=breaks.interval)
dev.off()


# bin by hour
breaks.interval <- "hour"

my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

print(length(my.table))

#  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

pdf(paste(figures.dir, "acf_", breaks.interval, "all_modes.pdf", sep=""))
acf(my.table, main=breaks.interval)
dev.off()


# bin by min
breaks.interval <- "min"

my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

print(length(my.table))

#  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

pdf(paste(figures.dir, "acf_", breaks.interval, "all_modes.pdf", sep=""))
acf(my.table, main=breaks.interval)
dev.off()



############################ WAVELET TRANSFORM ##########################


## breaks.interval = "mins"

## my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))
## time.series <- as.data.frame(my.table)
## myts <- as.ts(time.series$Freq)
## dwt1 <- dwt(myts)

## pdf(paste(figures.dir, "wavelet_transform_", breaks.interval, "all_modes.pdf", sep=""))
## plot(dwt1, main = paste("Discrete Wavelet Transform, All Modes"))
## dev.off()

## rm(list = ls())


####################### DIVIDE INTO DATE GROUPS, AUTOCORRELATION ###################

# divide events by date
start.date <- start.time
end.date <- end.time
num.groups <- 5

events.grouped <- group.data.by.date(events, start.date, end.date, num.groups)


# run autocorrelation on each group

for (group in 0:num.groups) {
#group <- 4

print(group)

  # subset events
  events <- subset(events.grouped, date.group == group)
  

                                        # make sure sorted in order of event
  events <- events[order(events$timestamp.event),]


  
  ## # bin by month
  ## breaks.interval <- "month"

  ## my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

  ## print(length(my.table))

  ##                                       #  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

  ## pdf(paste(figures.dir, "acf_group_", group, breaks.interval, "all_modes.pdf", sep="_"))
  ## acf(my.table, main=breaks.interval)
##  acf(my.table, main=paste("date group", group, breaks.interval))

  ## dev.off()

                                        # bin by week
  ## breaks.interval <- "week"

  ## my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

  ## print(length(my.table))

  ##                                       #  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

  ## pdf(paste(figures.dir, "acf_group_", group, breaks.interval, "all_modes.pdf", sep="_"))
  ## acf(my.table, main=breaks.interval)
##  acf(my.table, main=paste("date group", group, breaks.interval))

  ## dev.off()


                                        # bin by day
  breaks.interval <- "day"

  my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

  print(length(my.table))

                                        #  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

  pdf(paste(figures.dir, "acf_group_", group, breaks.interval, "all_modes.pdf", sep="_"))
  acf(my.table, main=paste("date group", group, breaks.interval))
  dev.off()


                                        # bin by hour
  breaks.interval <- "hour"

  my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

  print(length(my.table))

                                        #  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

  pdf(paste(figures.dir, "acf_group_", group, breaks.interval, "all_modes.pdf", sep="_"))
  acf(my.table, main=paste("date group", group, breaks.interval))
  dev.off()


                                        # bin by min
  breaks.interval <- "min"

  my.table <- table(cut(events$timestamp.event, breaks = breaks.interval))

  print(length(my.table))

                                        #  plot(my.table, type = "s", col = "black", xlab="Date", ylab="Number of Arrivals", main=paste("Arrivals (all modes) ", breaks.interval))

  pdf(paste(figures.dir, "acf_group_", group, breaks.interval, "all_modes.pdf", sep="_"))
  acf(my.table, main=paste("date group", group, breaks.interval))
  dev.off()

}



rm(list = ls())
