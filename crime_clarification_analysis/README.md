# Crime clarification analysis
This project analyzes crime reports in Uruguay, aiming to predict whether a case will be clarified using Probit regression models and to interpret causal effects. It includes an exploratory stage, data cleaning, evaluation of the model's performance, and causal inference.

# Data

The dataset is available [here](https://catalogodatos.gub.uy/dataset/ministerio-del-interior-delitos_denunciados_en_el_uruguay#).

The following are the columns of the dataset.

  

`ID_VICTIMA`: Id of the victim

  

`DEPARTAMENTO`, `JURISDICCION`,`LUGAR`: location.

  

`TIPO`: crime type.

  

`MOTIVO_APARENTE`: motive for the crime.

  

`FECHA`,`MES`,`HORA`, `DIA_SEMANA`, `TRIMESTRE`, `AÑO`: time.

  

`SEXO`, `EDADCALC`, `NACIONALIDAD`,`ANTECEDENTES`,`ANTECEDENTESPORESTUPEFACIENTES`: victim characteristics.

  

`ARMAREC`, `PROCESADOS`, `ACLARADO`: context of the crime.

  

`MENORESCINICIOPROC`: Minors involved

  

`REL_VICT_AGRES`: Relationship with the victim.

# Data processing

The data set has the shape [4163 rows x 22 columns].

  

First, I changed the date format to datetime64 type. Even though I dropped the following columns: TRIMESTRE(the trimester), DIA_SEMANA(day of the week), HORA(hour), AÑO(year), because they can already be infered by the date, I left MES(month) for further analysis.

  

Then I changed the SEXO column so that 0 represents male and 1 female.

  

For the ACLARADO variable, it was change to integrers too, of which 0 means the case was not clarified and 1 means it was clarified. 

  

Then, I converted several variables into dummies because we need categorical variables for the regression. The first column was dropped to avoid perfect multicollinearity

  
However, there seems to be a multicollinearity problem when running the probit model. This might be because there are too many categories that have a value of 1 only when the case was clarified(after creating the dummies).
In order to adress this, I merged all the 'department' variables except for the capital(MONTEVIDEO), because they had very few observations. Then dropped the column MENORESCINICIOPROC because it contained mostly NaN values.
I decided to drop the following columns due of quasi perfect correlatiton with ACLARADO: TIPO_A CLIENTE DE CAJERO / BANCO, TIPO_A TAXIS

## Model
The dependent variable, ACLARADO, as already discussed, takes the value 1 if the case was clarified and 0 otherwise. The Probit model is suitable for binary outcomes because it models the latent propensity of an event occurring and transforms it through a cumulative normal distribution to produce probabilities between 0 and 1.
``` 
         Current function value: 0.498612
         Iterations 6
                          Probit Regression Results
==============================================================================
Dep. Variable:               ACLARADO   No. Observations:                 3330
Model:                         Probit   Df Residuals:                     3302
Method:                           MLE   Df Model:                           27
Date:                Tue, 26 Aug 2025   Pseudo R-squ.:                  0.2603
Time:                        09:49:55   Log-Likelihood:                -1660.4
converged:                       True   LL-Null:                       -2244.7
Covariance Type:            nonrobust   LLR p-value:                3.806e-229
===============================================================================================================================
                                                                  coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------------------------------------------------
const                                                          -0.1383      0.605     -0.229      0.819      -1.323       1.047
SEXO                                                            0.2528      0.090      2.796      0.005       0.076       0.430
EDADCALC                                                       -0.0021      0.002     -1.198      0.231      -0.006       0.001
TIPO_A COMERCIO                                                -0.2529      0.298     -0.849      0.396      -0.837       0.331
TIPO_A MOTOCICLISTA                                            -0.6101      0.321     -1.901      0.057      -1.239       0.019
TIPO_A REPARTIDOR                                              -0.2277      0.396     -0.574      0.566      -1.004       0.549
TIPO_A TRANSEUNTE                                              -0.5101      0.297     -1.720      0.085      -1.091       0.071
TIPO_CASA DE FAMILIA                                           -0.7124      0.280     -2.541      0.011      -1.262      -0.163
TIPO_NO CORRESPONDE                                            -0.0831      0.599     -0.139      0.890      -1.257       1.090
TIPO_OTROS                                                     -0.1708      0.418     -0.409      0.683      -0.990       0.648
TIPO_SIN DATO                                                  -1.0086      0.613     -1.646      0.100      -2.210       0.192
MES_AGOSTO                                                     -0.0067      0.125     -0.053      0.957      -0.252       0.238
MES_DICIEMBRE                                                   0.0097      0.123      0.079      0.937      -0.232       0.251
MES_ENERO                                                      -0.0081      0.115     -0.070      0.944      -0.234       0.218
MES_FEBRERO                                                    -0.0575      0.120     -0.479      0.632      -0.293       0.178
MES_JULIO                                                      -0.0055      0.121     -0.045      0.964      -0.243       0.232
MES_JUNIO                                                      -0.1754      0.126     -1.392      0.164      -0.422       0.072
MES_MARZO                                                       0.0726      0.120      0.607      0.544      -0.162       0.307
MES_MAYO                                                       -0.1748      0.120     -1.460      0.144      -0.410       0.060
MES_NOVIEMBRE                                                   0.1922      0.125      1.541      0.123      -0.052       0.437
MES_OCTUBRE                                                    -0.1053      0.119     -0.882      0.378      -0.339       0.129
MES_SETIEMBRE                                                  -0.0856      0.124     -0.689      0.491      -0.329       0.158
MOTIVO_APARENTE_ALTERCADOS ESPONTANEOS/ CONFLICTOS DIVERSOS     1.2277      0.080     15.425      0.000       1.072       1.384
MOTIVO_APARENTE_OTROS MOTIVOS                                   1.1089      0.137      8.111      0.000       0.841       1.377
MOTIVO_APARENTE_RAPIÑA / HURTO / COPAMIENTO                     0.8808      0.546      1.614      0.107      -0.189       1.950
MOTIVO_APARENTE_SIN DATO/ DESCONOCIDO                          -0.8334      0.086     -9.677      0.000      -1.002      -0.665
MOTIVO_APARENTE_VIOLENCIA DOMESTICA Y ASOCIADOS                 1.4940      0.118     12.694      0.000       1.263       1.725
DEPARTAMENTO_OTROS                                              0.6049      0.053     11.435      0.000       0.501       0.709
===============================================================================================================================
```

# Performance
All this metrics are based on the assumption that if the probability is higher than 0.5, we predict 1, otherwise, we predict 0. This assumption comes from Wooldridge(2010).

The accuracy of the model is 76.4% (0.7647)

The following is the classification report:
```
              precision    recall  f1-score   support

           0       0.71      0.70      0.70       336
           1       0.80      0.81      0.80       497

    accuracy                           0.76       833
   macro avg       0.76      0.75      0.75       833
weighted avg       0.76      0.76      0.76       833
```

Again, 1 means cases clarified, 0 means cases not clarified.

- 71% of the cases predicted as not clarified were actually not clarified.

- The model correctly identified 70% of the cases that were actually not clarified.

- 80% of all the cases predicted as clarified were correct.

- The model correctly predicted 81% of all the real clarified cases.

The overall acuracy was 76% of all predictions, so 3 in 4 predictions are correct.

The F1 score is defined as F1score=2*(Precision*Recall)/(Precision+Recall)

The model has an average F1 score of 75%, which indicates a balance between minimizing false positives(Precision) and minimizing false negatives(recall). This can be infered from the formula above.


# Marginal effects
```
       Probit Marginal Effects       
=====================================
Dep. Variable:               ACLARADO
Method:                          dydx
At:                           overall
===============================================================================================================================
                                                                 dy/dx    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------------------------------------------------
SEXO                                                            0.0711      0.025      2.805      0.005       0.021       0.121
EDADCALC                                                       -0.0006      0.000     -1.199      0.231      -0.002       0.000
TIPO_A COMERCIO                                                -0.0712      0.084     -0.849      0.396      -0.235       0.093
TIPO_A MOTOCICLISTA                                            -0.1717      0.090     -1.904      0.057      -0.348       0.005
TIPO_A REPARTIDOR                                              -0.0641      0.111     -0.575      0.566      -0.283       0.154
TIPO_A TRANSEUNTE                                              -0.1435      0.083     -1.723      0.085      -0.307       0.020
TIPO_CASA DE FAMILIA                                           -0.2004      0.079     -2.549      0.011      -0.355      -0.046
TIPO_NO CORRESPONDE                                            -0.0234      0.168     -0.139      0.890      -0.354       0.307
TIPO_OTROS                                                     -0.0481      0.118     -0.409      0.683      -0.279       0.182
TIPO_SIN DATO                                                  -0.2838      0.172     -1.648      0.099      -0.621       0.054
MES_AGOSTO                                                     -0.0019      0.035     -0.053      0.957      -0.071       0.067
MES_DICIEMBRE                                                   0.0027      0.035      0.079      0.937      -0.065       0.071
MES_ENERO                                                      -0.0023      0.032     -0.070      0.944      -0.066       0.061
MES_FEBRERO                                                    -0.0162      0.034     -0.479      0.632      -0.082       0.050
MES_JULIO                                                      -0.0015      0.034     -0.045      0.964      -0.068       0.065
MES_JUNIO                                                      -0.0494      0.035     -1.393      0.164      -0.119       0.020
MES_MARZO                                                       0.0204      0.034      0.607      0.544      -0.045       0.086
MES_MAYO                                                       -0.0492      0.034     -1.461      0.144      -0.115       0.017
MES_NOVIEMBRE                                                   0.0541      0.035      1.542      0.123      -0.015       0.123
MES_OCTUBRE                                                    -0.0296      0.034     -0.883      0.377      -0.095       0.036
MES_SETIEMBRE                                                  -0.0241      0.035     -0.690      0.491      -0.093       0.044
MOTIVO_APARENTE_ALTERCADOS ESPONTANEOS/ CONFLICTOS DIVERSOS     0.3454      0.020     17.244      0.000       0.306       0.385
MOTIVO_APARENTE_OTROS MOTIVOS                                   0.3120      0.037      8.348      0.000       0.239       0.385
MOTIVO_APARENTE_RAPIÑA / HURTO / COPAMIENTO                     0.2478      0.153      1.616      0.106      -0.053       0.548
MOTIVO_APARENTE_SIN DATO/ DESCONOCIDO                          -0.2345      0.023    -10.103      0.000      -0.280      -0.189
MOTIVO_APARENTE_VIOLENCIA DOMESTICA Y ASOCIADOS                 0.4203      0.031     13.515      0.000       0.359       0.481
DEPARTAMENTO_OTROS                                              0.1702      0.014     12.135      0.000       0.143       0.198
===============================================================================================================================
       Probit Marginal Effects       
=====================================
Dep. Variable:               ACLARADO
Method:                          dydx
At:                           overall
===============================================================================================================================
                                                                 dy/dx    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------------------------------------------------
SEXO                                                            0.0706      0.025      2.840      0.005       0.022       0.119
EDADCALC                                                       -0.0006      0.000     -1.199      0.231      -0.002       0.000
TIPO_A COMERCIO                                                -0.0717      0.085     -0.846      0.397      -0.238       0.094
TIPO_A MOTOCICLISTA                                            -0.1732      0.089     -1.941      0.052      -0.348       0.002
TIPO_A REPARTIDOR                                              -0.0647      0.113     -0.571      0.568      -0.287       0.157
TIPO_A TRANSEUNTE                                              -0.1449      0.083     -1.740      0.082      -0.308       0.018
TIPO_CASA DE FAMILIA                                           -0.1996      0.075     -2.654      0.008      -0.347      -0.052
TIPO_NO CORRESPONDE                                            -0.0233      0.167     -0.139      0.889      -0.351       0.304
TIPO_OTROS                                                     -0.0485      0.119     -0.406      0.684      -0.282       0.185
TIPO_SIN DATO                                                  -0.2848      0.160     -1.779      0.075      -0.599       0.029
MES_AGOSTO                                                     -0.0019      0.035     -0.053      0.957      -0.071       0.067
MES_DICIEMBRE                                                   0.0027      0.035      0.079      0.937      -0.065       0.071
MES_ENERO                                                      -0.0023      0.032     -0.070      0.944      -0.066       0.061
MES_FEBRERO                                                    -0.0162      0.034     -0.478      0.633      -0.083       0.050
MES_JULIO                                                      -0.0015      0.034     -0.045      0.964      -0.068       0.065
MES_JUNIO                                                      -0.0498      0.036     -1.384      0.166      -0.120       0.021
MES_MARZO                                                       0.0203      0.033      0.610      0.542      -0.045       0.086
MES_MAYO                                                       -0.0496      0.034     -1.452      0.146      -0.117       0.017
MES_NOVIEMBRE                                                   0.0534      0.034      1.566      0.117      -0.013       0.120
MES_OCTUBRE                                                    -0.0298      0.034     -0.878      0.380      -0.096       0.037
MES_SETIEMBRE                                                  -0.0242      0.035     -0.687      0.492      -0.093       0.045
MOTIVO_APARENTE_ALTERCADOS ESPONTANEOS/ CONFLICTOS DIVERSOS     0.3255      0.017     19.378      0.000       0.293       0.358
MOTIVO_APARENTE_OTROS MOTIVOS                                   0.2707      0.025     10.690      0.000       0.221       0.320
MOTIVO_APARENTE_RAPIÑA / HURTO / COPAMIENTO                     0.2276      0.119      1.909      0.056      -0.006       0.461
MOTIVO_APARENTE_SIN DATO/ DESCONOCIDO                          -0.2490      0.026     -9.747      0.000      -0.299      -0.199
MOTIVO_APARENTE_VIOLENCIA DOMESTICA Y ASOCIADOS                 0.3580      0.019     19.125      0.000       0.321       0.395
DEPARTAMENTO_OTROS                                              0.1755      0.015     11.627      0.000       0.146       0.205
===============================================================================================================================
```

Acording to (Wooldridge 2010), in order to interpretate the results of the Probit model, we need the marginal values. We can calculate them with the function `model.get_margeff(at='overall', method='dydx')` This returns the average marginal effect of the variable over the dependent variable(ACLARADO)

- If the victim is a woman, the probability of the case being clarified increases on average by 7% (0.0706) with 95% confidence.

- If the crime occurs in a familiy home, the probability of the case being clarified decreases on average by 20% (-0.1996) with 95% confidence.

- If the crime motive is a spontaneous conflict between individuales, the probability of the case being clarified increases on average by 32.5% (0.3255) with 99% confidence.

- If the crime motive is domestic violence, the probability of the case being clarified increases on average by 35% (0.3580) with 99% confidence.

- If the reported crime occurred outside of the capital, the probability of the case being clarified increases on average by 18% (0.1755) with 99% confidence.

- The age of the victim doesn't seem to play a role on whether the case is clarified or not. (the p-value is 0.231)






# Second Model
This model adds an interaction between the variable SEXO(gender) and the dummy MOTIVO_APARENTE_VIOLENCIA DOMESTICA Y ASOCIADOS(domestic violence as the motive of the crime), to test the diference between male and female victims.
Also a square term for the age of the victim to test if cases where the victim is in a more vulnerable stage of life(young and older people) are more likely to be clarified.
```
       Probit Marginal Effects       
=====================================
Dep. Variable:               ACLARADO
Method:                          dydx
At:                           overall
===============================================================================================================================
                                                                 dy/dx    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------------------------------------------------
SEXO                                                            0.0449      0.028      1.597      0.110      -0.010       0.100
EDADCALC                                                        0.0019      0.002      1.249      0.212      -0.001       0.005
TIPO_A COMERCIO                                                -0.0653      0.084     -0.781      0.435      -0.229       0.098
TIPO_A MOTOCICLISTA                                            -0.1682      0.090     -1.871      0.061      -0.344       0.008
TIPO_A REPARTIDOR                                              -0.0650      0.111     -0.585      0.558      -0.283       0.153
TIPO_A TRANSEUNTE                                              -0.1327      0.083     -1.596      0.110      -0.296       0.030
TIPO_CASA DE FAMILIA                                           -0.1711      0.080     -2.151      0.031      -0.327      -0.015
TIPO_NO CORRESPONDE                                             0.0115      0.174      0.066      0.947      -0.329       0.352
TIPO_OTROS                                                     -0.0405      0.118     -0.345      0.730      -0.271       0.190
TIPO_SIN DATO                                                  -0.2488      0.177     -1.405      0.160      -0.596       0.098
MES_AGOSTO                                                      0.0003      0.035      0.010      0.992      -0.069       0.069
MES_DICIEMBRE                                                   0.0052      0.035      0.150      0.881      -0.063       0.073
MES_ENERO                                                      -0.0003      0.032     -0.010      0.992      -0.064       0.063
MES_FEBRERO                                                    -0.0141      0.034     -0.418      0.676      -0.080       0.052
MES_JULIO                                                      -0.0004      0.034     -0.013      0.990      -0.067       0.066
MES_JUNIO                                                      -0.0466      0.035     -1.313      0.189      -0.116       0.023
MES_MARZO                                                       0.0222      0.034      0.662      0.508      -0.044       0.088
MES_MAYO                                                       -0.0473      0.034     -1.407      0.159      -0.113       0.019
MES_NOVIEMBRE                                                   0.0550      0.035      1.571      0.116      -0.014       0.124
MES_OCTUBRE                                                    -0.0266      0.034     -0.793      0.428      -0.092       0.039
MES_SETIEMBRE                                                  -0.0218      0.035     -0.625      0.532      -0.090       0.047
MOTIVO_APARENTE_ALTERCADOS ESPONTANEOS/ CONFLICTOS DIVERSOS     0.3447      0.020     17.272      0.000       0.306       0.384
MOTIVO_APARENTE_OTROS MOTIVOS                                   0.3194      0.037      8.552      0.000       0.246       0.393
MOTIVO_APARENTE_RAPIÑA / HURTO / COPAMIENTO                     0.2781      0.159      1.750      0.080      -0.033       0.590
MOTIVO_APARENTE_SIN DATO/ DESCONOCIDO                          -0.2306      0.023     -9.949      0.000      -0.276      -0.185
MOTIVO_APARENTE_VIOLENCIA DOMESTICA Y ASOCIADOS                 0.3671      0.039      9.423      0.000       0.291       0.443
DEPARTAMENTO_OTROS                                              0.1695      0.014     12.087      0.000       0.142       0.197
SEXO_x_VIOLENCIA                                                0.1664      0.069      2.402      0.016       0.031       0.302
EDADCALC_sq                                                 -2.936e-05   1.74e-05     -1.686      0.092   -6.35e-05    4.77e-06
===============================================================================================================================
       Probit Marginal Effects       
=====================================
Dep. Variable:               ACLARADO
Method:                          dydx
At:                           overall
===============================================================================================================================
                                                                 dy/dx    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------------------------------------------------
SEXO                                                            0.0447      0.028      1.609      0.108      -0.010       0.099
EDADCALC                                                        0.0019      0.002      1.249      0.212      -0.001       0.005
TIPO_A COMERCIO                                                -0.0657      0.084     -0.780      0.436      -0.231       0.100
TIPO_A MOTOCICLISTA                                            -0.1693      0.089     -1.912      0.056      -0.343       0.004
TIPO_A REPARTIDOR                                              -0.0656      0.113     -0.583      0.560      -0.286       0.155
TIPO_A TRANSEUNTE                                              -0.1338      0.083     -1.611      0.107      -0.297       0.029
TIPO_CASA DE FAMILIA                                           -0.1708      0.077     -2.215      0.027      -0.322      -0.020
TIPO_NO CORRESPONDE                                             0.0115      0.174      0.066      0.947      -0.330       0.353
TIPO_OTROS                                                     -0.0408      0.119     -0.343      0.731      -0.274       0.192
TIPO_SIN DATO                                                  -0.2505      0.169     -1.486      0.137      -0.581       0.080
MES_AGOSTO                                                      0.0003      0.035      0.010      0.992      -0.069       0.069
MES_DICIEMBRE                                                   0.0052      0.035      0.150      0.880      -0.063       0.073
MES_ENERO                                                      -0.0003      0.032     -0.010      0.992      -0.064       0.063
MES_FEBRERO                                                    -0.0141      0.034     -0.417      0.677      -0.081       0.052
MES_JULIO                                                      -0.0004      0.034     -0.013      0.990      -0.067       0.066
MES_JUNIO                                                      -0.0469      0.036     -1.305      0.192      -0.117       0.024
MES_MARZO                                                       0.0222      0.033      0.665      0.506      -0.043       0.087
MES_MAYO                                                       -0.0477      0.034     -1.399      0.162      -0.114       0.019
MES_NOVIEMBRE                                                   0.0544      0.034      1.594      0.111      -0.012       0.121
MES_OCTUBRE                                                    -0.0267      0.034     -0.789      0.430      -0.093       0.040
MES_SETIEMBRE                                                  -0.0219      0.035     -0.622      0.534      -0.091       0.047
MOTIVO_APARENTE_ALTERCADOS ESPONTANEOS/ CONFLICTOS DIVERSOS     0.3256      0.017     19.369      0.000       0.293       0.358
MOTIVO_APARENTE_OTROS MOTIVOS                                   0.2760      0.025     11.069      0.000       0.227       0.325
MOTIVO_APARENTE_RAPIÑA / HURTO / COPAMIENTO                     0.2509      0.116      2.161      0.031       0.023       0.478
MOTIVO_APARENTE_SIN DATO/ DESCONOCIDO                          -0.2439      0.025     -9.628      0.000      -0.294      -0.194
MOTIVO_APARENTE_VIOLENCIA DOMESTICA Y ASOCIADOS                 0.3212      0.027     12.118      0.000       0.269       0.373
DEPARTAMENTO_OTROS                                              0.1747      0.015     11.587      0.000       0.145       0.204
SEXO_x_VIOLENCIA                                                0.1582      0.060      2.625      0.009       0.040       0.276
EDADCALC_sq                                                 -2.936e-05   1.74e-05     -1.686      0.092   -6.35e-05    4.77e-06
===============================================================================================================================
```


```
accuracy: 0.7623049219687875
[[234 102]
 [ 96 401]]
              precision    recall  f1-score   support

           0       0.71      0.70      0.70       336
           1       0.80      0.81      0.80       497

    accuracy                           0.76       833
   macro avg       0.75      0.75      0.75       833
weighted avg       0.76      0.76      0.76       833
```

The accuracy of this model is 0.762, and the precision, recall and therefore F1-score metrics are nearly identical to the first model.

The marginal effects of the already discussed variables are very similar if not identical.

- Female victims are on average 15.8% (0.1582) more likely to have their cases clarified compared to male victims, with 95% confidence. For male victims in domestic violence cases, the probability of clarification is simply the marginal effect of the domestic violence variable itself, that is an increase on average by 32.1% (0.3212) over the probability of case being clarified, with 99% confidence.
- The effect of the squared victim's age term is significant with a p-value of 0.092 (at 10% significance) but the impact on the probability of the case being clarified is marginal.


# Sources
- Wooldridge, Jeffrey M.(2010) Introductory Econometrics, Fourth Edition

# Annex
<img width="500" height="254" alt="Figure_1" src="https://github.com/user-attachments/assets/808400ce-519f-484e-902c-040bc023c88f" />
<img width="500" height="254" alt="Figure_2" src="https://github.com/user-attachments/assets/ff8698c3-dc92-4245-bfd4-f9ab82948cba" />
<img width="500" height="254" alt="Figure_3" src="https://github.com/user-attachments/assets/005596ca-e38f-421c-a097-66ee6ec5cf71" />
<img width="500" height="254" alt="Figure_4" src="https://github.com/user-attachments/assets/8373ade2-5b91-42aa-be3e-2e813fe7cf1f" />
<img width="500" height="254" alt="Figure_5" src="https://github.com/user-attachments/assets/f38db72d-c121-48f7-90a6-d698d5c72ca2" />
<img width="500" height="254" alt="Figure_6" src="https://github.com/user-attachments/assets/f2d1382a-b762-4298-b680-e9d0edf00f71" />
<img width="500" height="254" alt="Figure_7" src="https://github.com/user-attachments/assets/c712a852-2aee-437f-8bad-8837cdd9896a" />
