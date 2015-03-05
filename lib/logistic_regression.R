
mydata <- read.csv("/Users/marten/Downloads/wsd_logistic_regression/output/logistic_regression/sval2_sval3+++n_v_a+++num_senses---pos.csv")
mylogit <- glm(correct ~ num_senses + pos, data = mydata, family =  binomial("logit"))
summary(mylogit)