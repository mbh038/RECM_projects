# Hukseflux heat Flux Meter
rhfm=0.00625 # W/m2
  
# amplifier functions
ampch1<-function(vout){
    0.012 * vout - 0.094 #cal 5-02-16 alice & mike
}
ampch2<-function(vout){
    0.0118 * vout - 0.5235 #cal 5-02-16 alice & mike
}

# heat flux function

Qt<-function(R1,R2,Tm_init,C){
    Tm[1]=Tm_init
    for (i in 1:(length(t)-1)){
        dt=60*(t[i+1]-t[i])
        Q[i]=(Tint[i]-Tm[i])/R1
        Tm[i+1]=((Tint[i+1]/R1)+(Text[i+1]/R2)+C*Tm[i]/dt)/(1/R1 + 1/R2 + C/dt)
    }
    Q
}

### Bamboo House April 2017

u4p<-read.table("BambooHouse003.csv",sep=",",stringsAsFactors=FALSE,header=TRUE)
id<-seq(1,nrow(u4p))
u4p<-cbind(id,u4p)
names(u4p)<-c("id","datetime","T1","T2","hp1") #T1 is in, T2 is out

ymax=max(u4p$T1,na.rm=TRUE)
ymin=min(u4p$T2,na.rm=TRUE)

library(rafalib)
mypar(2,1)
plot(u4p$T2,type="l",ylim=c(ymin,ymax)) # outside
lines(u4p$T1,col=2) # inside


# heat plate plots
u4p$hp1preamp1<-ampch1(u4p$hp1)
u4p$hp1flux1<-u4p$hp1preamp1/0.06


index=200:(nrow(u4p)-20)
plot(u4p$id[index],u4p$hp1[index],type="l")


plot(u4p$id[index],u4p$hp1flux1[index],type="l")


Qexp<-u4p$hp1flux1[index]
Qexp<- -Qexp[-1]+15
Tint<-u4p$T1[index]
Text<-u4p$T2[index]
t=u4p$id[index]

Tm=numeric()
Q=numeric()

mypar(1,1)
R1=0.4
R2=0.4
C=1364
Tm_init=10
tau=60

Q<-Qt(R1,R2,Tm_init,C)


plot(Qexp,type="l",ylim=c(min(min(Q),min(Qexp)),max(max(Q),max(Qexp))),xlab="Time (min)",ylab="Heat flux Q (W/m^2)",col="red")
lines(Q,col="blue")
legend("topright", c("Measured", "Predicted"), pch="o", col=c("red", "blue"))

LL <- function(R1,R2,Tm_init,C, mu, sigma) {
    R = Qexp-Qt(R1,R2,Tm_init,C)
    #
    R = suppressWarnings(dnorm(R, mu, sigma, log = TRUE))
    #
    -sum(R)
}


library(stats4)
fit4p<-mle(LL, 
           start = list(R1=0.4,R2=0.4,Tm_init=10,C=1364,sigma=1),
           fixed=list(mu=0),
           nobs = length(Q),
           lower = c(.01,.01,1,1000,0.1), 
           upper = c(2,2.,17,2000000,5),
           method= "L-BFGS-B"
)

Q<-Qt(coef(fit4p)[1],coef(fit4p)[2],coef(fit4p)[3],coef(fit4p)[4])
lines(Q,col="green")

summary(fit4p)

U4bare=1/(coef(fit4p)[1]+coef(fit4p)[2]-rhfm)
U4bare

