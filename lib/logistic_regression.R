
mydata <- read.csv("/Users/marten/git/WSD_error_analysis/output/logistic_regression/gs_sval2013+++n_v_r_a+++len_sentence---avg_num_senses_in_sentence---num_senses---pos---rel_freq---total_occurences---occurs_in_x_num_docs.csv")
mylogit <- glm(correct ~ len_sentence + avg_num_senses_in_sentence + num_senses + pos + rel_freq + total_occurences + occurs_in_x_num_docs, data = mydata, family =  binomial("logit"))
summary(mylogit)