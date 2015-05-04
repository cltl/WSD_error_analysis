
mydata <- read.csv("CSV_INPUT")
mylogit <- glm(correct ~ VARIABLES, data = mydata, family =  binomial("logit"))
summary(mylogit)