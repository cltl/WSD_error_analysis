
mydata <- read.csv("CSV_INPUT")
glm1 <- glm(correct ~ VARIABLES, data = mydata, family =  binomial("logit"))

summary(glm1)

#with(glm1, null.deviance - deviance)
#with(glm1, df.null - df.residual)
#with(glm1, pchisq(null.deviance - deviance, df.null - df.residual, lower.tail = FALSE))


R2<-1-((glm1$deviance/-2)/(glm1$null.deviance/-2))
cat("mcFadden R2=",R2,"\n")

#R2<-1-exp((glm1$deviance-glm1$null.deviance)/2*n)
#cat("Cox-Snell R2=",R2,"\n")

#R2<-R2/(1-exp((-glm1$null.deviance)/n))
#cat("Nagelkerke R2=",R2,"\n")

#AIC<- glm1$deviance+2*2
#cat("AIC=",AIC,"\n")