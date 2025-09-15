# Model selection

| model       | acc | sensitivity  | balanced acc | details             |
| --- | --- | --- | ---- | --- |
| log1     | 0.74     | 0.82                | 0.68              | complete  |
| log2     | 0.745    | 0.92                | 0.62              | reduced  |
| rf1        | 0.77     | 0.94                | 0.65              | ntree=500, mtry=3 complete |
| rf2        | 0.80     | 0.89               | 0.73              | ntree=400, mtry=5 complete |
| NB | 0.65     | 0.63                | 0.66              | complete          |


# Selected model
### Random forest model 2
```
> #random forest
> set.seed(42)
> model_rf <- randomForest(as.factor(creditrisk) ~ ., data = train, ntree = 400, mtry = 5, importance = TRUE)

Confusion Matrix and Statistics

          Reference
Prediction   0   1
         0 127  25
         1  15  33
                                          
               Accuracy : 0.8             
                 95% CI : (0.7378, 0.8531)
    No Information Rate : 0.71            
    P-Value [Acc > NIR] : 0.002456        
                                          
                  Kappa : 0.4882          
                                          
 Mcnemar's Test P-Value : 0.154729        
                                          
            Sensitivity : 0.8944          
            Specificity : 0.5690          
         Pos Pred Value : 0.8355          
         Neg Pred Value : 0.6875          
             Prevalence : 0.7100          
         Detection Rate : 0.6350          
   Detection Prevalence : 0.7600          
      Balanced Accuracy : 0.7317          
                                          
       'Positive' Class : 0               
                                          
> 
> acc_rf <- mean(y_pred_rf == test$creditrisk)
> acc_rf
[1] 0.8
```
Random forest model 2 was selected because it has the highest and most balanced accuracy among the remaining models. Also, after running it with different seeds we get an average accuracy of 0.7485 +- 0.02439. The low accuracy standard deviation means its performance is stable, due of the low accuracy standard deviation.

The sensitivity level(0.8944) means about 89% of non risky individuals are correctly classified.
After running the same model with Python, we get the following classification report:
```
accuracy: 0.775
              precision    recall  f1-score   support

           0       0.77      0.96      0.86       140
           1       0.80      0.33      0.47        60

    accuracy                           0.78       200
   macro avg       0.79      0.65      0.66       200
weighted avg       0.78      0.78      0.74       200
```

Which means 77.5% of all test samples were correctly classified, but we have to consider the balance of the sample. 140 obervations are non-risky, while 60 are risky, which might reduce the importance of the accuracy score interpretation. The model correctly identifies 96% of actual non-risky individuals and 33% of actual risky individuals. So naturally, the model is better predictinig non risky individuals.

<img width="535" height="360" alt="fig1" src="https://github.com/user-attachments/assets/e984c184-e2ef-49fe-bace-9b6c55470c39" />


# Other models

### Logit model 1
```
f <- as.formula(paste("creditrisk ~", statusA11 + statusA12 + statusA13 + statusA14 + duration + credithistoryA31 + credithistoryA32 + credithistoryA33 + credithistoryA34 + purposeA41 + purposeA410 + purposeA42 + purposeA43 + purposeA44 + purposeA45 + purposeA46 + purposeA48 + purposeA49 + savingsA62 + savingsA63 + savingsA64 + savingsA65 + employmentsinceA72 + employmentsinceA73 + employmentsinceA74 + employmentsinceA75 + installmentrate + personalstatusA92 + personalstatusA93 + personalstatusA94 + otherdebtorsA102 + otherdebtorsA103 + residencesince + propertyA122 + propertyA123 + propertyA124 + age + otherinstallmentplansA142 + otherinstallmentplansA143 + housingA152 + housingA153 + existingcredits2 + existingcredits3 + existingcredits4 + jobA172 + jobA173 + jobA174 + liable + telephoneA192 + foreignworkerA202))
Confusion Matrix and Statistics

          Reference
Prediction   0   1
         0 116  26
         1  26  32
                                          
               Accuracy : 0.74            
                 95% CI : (0.6734, 0.7993)
    No Information Rate : 0.71            
    P-Value [Acc > NIR] : 0.1965          
                                          
                  Kappa : 0.3686          
                                          
 Mcnemar's Test P-Value : 1.0000          
                                          
            Sensitivity : 0.8169          
            Specificity : 0.5517          
         Pos Pred Value : 0.8169          
         Neg Pred Value : 0.5517          
             Prevalence : 0.7100          
         Detection Rate : 0.5800          
   Detection Prevalence : 0.7100          
      Balanced Accuracy : 0.6843          
                                          
       'Positive' Class : 0               
                                          
> 
> acc <- mean(y_pred == test$creditrisk)
> acc
[1] 0.74
> AIC(model_1)
[1] 791.5057
```
### Logit model 2
```
f <- as.formula(paste("creditrisk ~", "duration + credithistoryA30 + credithistoryA31 + credithistoryA32 + credithistoryA33 + credithistoryA34 + savingsA62 + savingsA63 + savingsA64 + savingsA65 + installmentrate + residencesince + propertyA122 + propertyA123 + propertyA124 + age + jobA172 + jobA173 + jobA174 + liable"))
Confusion Matrix and Statistics

          Reference
Prediction   0   1
         0 130  39
         1  12  19
                                          
               Accuracy : 0.745           
                 95% CI : (0.6787, 0.8039)
    No Information Rate : 0.71            
    P-Value [Acc > NIR] : 0.1554396       
                                          
                  Kappa : 0.2819          
                                          
 Mcnemar's Test P-Value : 0.0002719       
                                          
            Sensitivity : 0.9155          
            Specificity : 0.3276          
         Pos Pred Value : 0.7692          
         Neg Pred Value : 0.6129          
             Prevalence : 0.7100          
         Detection Rate : 0.6500          
   Detection Prevalence : 0.8450          
      Balanced Accuracy : 0.6215          
                                          
       'Positive' Class : 0               
                                          
> 
> acc <- mean(y_pred == test$creditrisk)
> acc
[1] 0.745
> AIC(model_1)
[1] 881.5113
```

### Random forest model 1
```
> #random forest
> set.seed(42)
model_rf <- randomForest(as.factor(creditrisk) ~ ., data = train, ntree = 500, mtry = 3, importance = TRUE)
Confusion Matrix and Statistics

          Reference
Prediction   0   1
         0 133  37
         1   9  21
                                          
               Accuracy : 0.77            
                 95% CI : (0.7054, 0.8264)
    No Information Rate : 0.71            
    P-Value [Acc > NIR] : 0.0344          
                                          
                  Kappa : 0.3484          
                                          
 Mcnemar's Test P-Value : 6.865e-05       
                                          
            Sensitivity : 0.9366          
            Specificity : 0.3621          
         Pos Pred Value : 0.7824          
         Neg Pred Value : 0.7000          
             Prevalence : 0.7100          
         Detection Rate : 0.6650          
   Detection Prevalence : 0.8500          
      Balanced Accuracy : 0.6493          
                                          
       'Positive' Class : 0               
                                          
> 
> acc_rf <- mean(y_pred_rf == test$creditrisk)
> acc_rf
[1] 0.77
```

### Naive bayes model 1
```
> ###############
> #naive bayes
> 
> model_nb <- naiveBayes(as.factor(creditrisk) ~ ., data = train)
> 
> y_pred_nb <- predict(model_nb, newdata = test)
> 
> cm_nb <- confusionMatrix(factor(y_pred_nb), factor(test$creditrisk))
> cm_nb
Confusion Matrix and Statistics

          Reference
Prediction  0  1
         0 90 18
         1 52 40
                                          
               Accuracy : 0.65            
                 95% CI : (0.5795, 0.7159)
    No Information Rate : 0.71            
    P-Value [Acc > NIR] : 0.9726          
                                          
                  Kappa : 0.2757          
                                          
 Mcnemar's Test P-Value : 8.005e-05       
                                          
            Sensitivity : 0.6338          
            Specificity : 0.6897          
         Pos Pred Value : 0.8333          
         Neg Pred Value : 0.4348          
             Prevalence : 0.7100          
         Detection Rate : 0.4500          
   Detection Prevalence : 0.5400          
      Balanced Accuracy : 0.6617          
                                          
       'Positive' Class : 0               
                                          
> 
> acc_nb <- mean(y_pred_nb == test$creditrisk)
> acc_nb
[1] 0.65
```
