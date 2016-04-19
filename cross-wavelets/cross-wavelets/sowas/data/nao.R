A <- matrix(scan("nao.dat",comment.char="#"),ncol=2,byrow=TRUE)

Adum <- A

Adum[is.na(Adum)] <- 0

t <- Adum %*% c(1,0)
x <- A %*% c(0,1)

N=length(t)
  
nao<-stats::ts(data=x,start=t[1],frequency=12)
