install.packages('readr')
install.packages('dplyr')
install.packages('caret')
install.packages("randomForest")
install.packages("e1071")
library(e1071)
library(randomForest)
library(readr)
library(dplyr)
library(caret)
library(ggplot2)

#load data
df <- read_csv("D:/DataScience/projects/6/data/german.csv")
#cat var
categorical_1 <- c("credithistory", "savings", "property", "job", "purpose", "employmentsince", 
                 "personalstatus", "otherdebtors", "otherinstallmentplans", 
                 "existingcredits", "housing","telephone","status", "foreignworker")
categorical_2 <- c("credithistory", "savings", "property", "job")

to_drop_1 <- c("credit")
to_drop_2 <- c("status","credit", "purpose", "employmentsince", 
               "personalstatus", "otherdebtors", "otherinstallmentplans", 
               "existingcredits", "housing","telephone", "foreignworker")

#drop
df <- df %>% select(-all_of(to_drop_1))
#dummies
df[categorical_1] <- lapply(df[categorical_1], as.factor)

#binary creditrisk
df$creditrisk <- ifelse(df$creditrisk == 1, 0, 1)
#separate data
y <- df$creditrisk
X <- df %>% select(-creditrisk)
X_matrix <- model.matrix(~ . -1, data = X)
data <- as.data.frame(cbind(X_matrix, creditrisk = y))
ncol(X_matrix)
#test split
set.seed(42)
trainIndex <- createDataPartition(data$creditrisk, p = 0.8, list = FALSE)
train <- data[trainIndex, ]
test <- data[-trainIndex, ]

#logit
f <- as.formula(paste("creditrisk ~", paste(colnames(X_matrix), collapse = " + ")))
model_1 <- glm(f, data = train, family = binomial(link = "logit"))
paste(colnames(X_matrix), collapse = " + ")

y_pred_prob <- predict(model_1, newdata = test, type = "response")
y_pred <- ifelse(y_pred_prob > 0.5, 1, 0)

table(y_pred)
table(test$creditrisk)

cm <- confusionMatrix(factor(y_pred), factor(test$creditrisk))
cm

acc <- mean(y_pred == test$creditrisk)
acc
AIC(model_1)

##################
#random forest
set.seed(42)
model_rf <- randomForest(as.factor(creditrisk) ~ ., data = train, ntree = 400, mtry = 5, importance = TRUE)

y_pred_rf <- predict(model_rf, newdata = test)

cm_rf <- confusionMatrix(y_pred_rf, factor(test$creditrisk))
cm_rf

acc_rf <- mean(y_pred_rf == test$creditrisk)
acc_rf

varImpPlot(model_rf)

###############
#naive bayes
model_nb <- naiveBayes(as.factor(creditrisk) ~ ., data = train, laplace=5)

y_pred_nb <- predict(model_nb, newdata = test)

cm_nb <- confusionMatrix(factor(y_pred_nb), factor(test$creditrisk))
cm_nb

acc_nb <- mean(y_pred_nb == test$creditrisk)
acc_nb
