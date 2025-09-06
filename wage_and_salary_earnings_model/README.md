# Wage and salary earnings multivariate linear regression
The objective of this project is to build a regression model that explains variations in wages across industries and demographics for the US, including processing the dataset, evaluating the model and interpreting the coefficients .

The results are that wages increase with age, education, hours worked, and in some industries. Women earn on average less than men, ceteris paribus. Being married, capital income, and better health are all associated with higher wages. Being foreign born(not US citizen), earning alternative income sources, poor health, larger households, and hourly work are associated with lower wage and salary earnings. Race doesn't seem to be significant.

# Data
The data is available [here](https://www.census.gov/programs-surveys/cps/data.html ) 

The data contains three tables: Household, Familiy and Person.

According to the documentation:
"This Annual Social and Economic (ASEC) Supplement provides the usual monthly labor force data, but in addition, provides supplemental data on work experience, income, noncash benefits, and migration. Comprehensive work experience information is given on the employment status,
occupation, and industry of persons 15 years old and over. Additional data for persons 15 years old and older are available concerning weeks worked and hours per week worked, reason not working full time,
total income and income components. Data on employment and income refer to the preceding year,
although demographic data refer to the time of the
survey.

This file also contains data covering nine noncash income sources: food stamps, school lunch program, employer-provided group health insurance plan, employer-provided pension plan, personal health insurance, Medicaid, Medicare, or military health care, and energy assistance. Characteristics such as age, sex, race, household relationship, and Hispanic origin are shown for each person in the household enumerated."
(Current Population Survey, 2024 ASEC Technical Documentation)

This are the selected variables from the dataset: 
- WSAL_VAL: Total wage and salary earnings
- A_AGE: Age
- A_SEX: Sex
- A_HGA: Education attainment
- A_MARITL: Marital status
- PRDTRACE: Race
- PRCITSHP: Citizenship
- A_HRS1: Hours worked last week
- A_MJIND: Industry code
- A_HRLYWK: Is paid by the hour?
- WORKYN: Worked during year 2020
- LKWEEKS: weeks looking for job
- ERN_SRCE: Source of earnings
- CAP_YN: Capital gains received?
- ED_YN: Educational assistance receive?
- FIN_YN: Financial assistance recive?
- CSP_YN child support payments recive?
- HEA: Health status
- H_NUMPER: Number of persons in household

# Data processing and modeling
```
SELECT 
WSAL_VAL, log(WSAL_VAL) as WSAL_VAL_log, A_AGE, (A_AGE*A_AGE) as A_AGE_SQ, A_SEX, A_HGA, A_MARITL, PRDTRACE, 
PRCITSHP, A_HRS1, A_MJIND, A_HRLYWK, WORKYN, LKWEEKS, ERN_SRCE, CAP_YN, ED_YN, FIN_YN, CSP_YN, HEA, H_NUMPER
FROM pppub 
```
First, the dependent variable was transformed into logarithm. A squared term for the age was added because the people's income is generally lower on their youth and as they age pass their adulthood. Interaction terms will be added later on python because these are categorical variables and their values are meaningless right now.

```
LEFT JOIN hhpub ON substr(pppub.PERIDNUM,1 , 20) = hhpub.H_IDNUM
```
We join pppub with the hhpub table, which contains information about the households. According to the data dictionary(ASEC 2024 Public Use Data Dictionary), PERIDNUM is the unique id of the individual and H_IDNUM is the household id number. Which is the same as the first 1-20 characters of PERIDNUM. That's why the characters are substracted. Also, in case the tables have different total rows, LEFT JOIN includes rows from A regardless of whether B has a matching row.
```
WHERE CAST(WSAL_VAL AS NUMERIC) > 0;
```
And because we are working with individuals who are currently in the labor force, we can filter out the ones without wages. Also, this allows the use of logarithm in the dependent variable.

The first model is the following:
```
                           OLS Regression Results
==============================================================================
Dep. Variable:           WSAL_VAL_log   R-squared:                       0.471
Model:                            OLS   Adj. R-squared:                  0.470
Method:                 Least Squares   F-statistic:                     752.6
Date:                Thu, 04 Sep 2025   Prob (F-statistic):               0.00
Time:                        23:36:52   Log-Likelihood:                -26079.
No. Observations:               69489   AIC:                         5.232e+04
Df Residuals:                   69406   BIC:                         5.308e+04
Df Model:                          82
Covariance Type:            nonrobust
=====================================================================================
                        coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------
const                 3.2108      0.042     75.790      0.000       3.128       3.294
A_AGE                 0.0373      0.001     60.137      0.000       0.036       0.039
A_AGE_SQ             -0.0004   6.55e-06    -58.214      0.000      -0.000      -0.000
A_HRS1                0.0066   9.69e-05     68.400      0.000       0.006       0.007
LKWEEKS              -0.0114      0.000    -42.085      0.000      -0.012      -0.011
H_NUMPER             -0.0140      0.001    -14.797      0.000      -0.016      -0.012
A_SEX_2              -0.0545      0.008     -6.567      0.000      -0.071      -0.038
PRDTRACE_2           -0.0180      0.004     -4.051      0.000      -0.027      -0.009
PRDTRACE_3           -0.0122      0.011     -1.065      0.287      -0.035       0.010
PRDTRACE_4            0.0343      0.006      6.108      0.000       0.023       0.045
PRDTRACE_5            0.0077      0.018      0.427      0.669      -0.028       0.043
PRDTRACE_6            0.0085      0.016      0.538      0.591      -0.022       0.039
PRDTRACE_7           -0.0044      0.015     -0.283      0.777      -0.035       0.026
PRDTRACE_8           -0.0318      0.019     -1.713      0.087      -0.068       0.005
PRDTRACE_9            0.0305      0.039      0.778      0.437      -0.046       0.107
PRDTRACE_10          -0.0251      0.048     -0.523      0.601      -0.119       0.069
PRDTRACE_11           0.0431      0.074      0.585      0.558      -0.101       0.187
PRDTRACE_12           0.2675      0.106      2.517      0.012       0.059       0.476
PRDTRACE_13          -0.1115      0.144     -0.775      0.438      -0.394       0.171
PRDTRACE_15          -0.0095      0.043     -0.223      0.824      -0.093       0.074
PRDTRACE_16          -0.0265      0.050     -0.525      0.599      -0.125       0.072
PRDTRACE_17          -0.2329      0.091     -2.558      0.011      -0.411      -0.054
PRDTRACE_19           0.0711      0.144      0.494      0.621      -0.211       0.353
PRDTRACE_20           0.1606      0.353      0.456      0.649      -0.530       0.852
PRDTRACE_21           0.0428      0.047      0.908      0.364      -0.050       0.135
PRDTRACE_23          -0.0369      0.353     -0.105      0.917      -0.728       0.654
PRDTRACE_25           0.1002      0.352      0.284      0.776      -0.591       0.791
PRDTRACE_26          -0.0730      0.094     -0.775      0.438      -0.258       0.112
PRCITSHP_2           -0.0323      0.019     -1.731      0.083      -0.069       0.004
PRCITSHP_3           -0.0099      0.014     -0.723      0.470      -0.037       0.017
PRCITSHP_4           -0.0079      0.005     -1.548      0.122      -0.018       0.002
PRCITSHP_5           -0.0602      0.005    -11.769      0.000      -0.070      -0.050
A_HGA_32             -0.0204      0.040     -0.505      0.613      -0.100       0.059
A_HGA_33             -0.0250      0.037     -0.675      0.500      -0.098       0.048
A_HGA_34             -0.0361      0.037     -0.976      0.329      -0.109       0.036
A_HGA_35             -0.1429      0.036     -3.925      0.000      -0.214      -0.072
A_HGA_36             -0.1673      0.036     -4.626      0.000      -0.238      -0.096
A_HGA_37             -0.1523      0.036     -4.246      0.000      -0.223      -0.082
A_HGA_38             -0.0805      0.036     -2.209      0.027      -0.152      -0.009
A_HGA_39              0.0672      0.035      1.939      0.052      -0.001       0.135
A_HGA_40              0.0906      0.035      2.605      0.009       0.022       0.159
A_HGA_41              0.1264      0.035      3.595      0.000       0.057       0.195
A_HGA_42              0.1229      0.035      3.511      0.000       0.054       0.192
A_HGA_43              0.2267      0.035      6.528      0.000       0.159       0.295
A_HGA_44              0.2956      0.035      8.477      0.000       0.227       0.364
A_HGA_45              0.4437      0.036     12.191      0.000       0.372       0.515
A_HGA_46              0.4018      0.036     11.249      0.000       0.332       0.472
A_MARITL_2           -0.0524      0.023     -2.270      0.023      -0.098      -0.007
A_MARITL_3           -0.0496      0.011     -4.517      0.000      -0.071      -0.028
A_MARITL_4           -0.0516      0.010     -5.076      0.000      -0.072      -0.032
A_MARITL_5           -0.0483      0.005     -9.637      0.000      -0.058      -0.039
A_MARITL_6           -0.0649      0.010     -6.240      0.000      -0.085      -0.045
A_MARITL_7           -0.0728      0.004    -18.860      0.000      -0.080      -0.065
A_MJIND_1             0.0875      0.014      6.222      0.000       0.060       0.115
A_MJIND_2             0.2766      0.020     13.520      0.000       0.237       0.317
A_MJIND_3             0.1986      0.008     23.424      0.000       0.182       0.215
A_MJIND_4             0.1854      0.008     22.974      0.000       0.170       0.201
A_MJIND_5             0.0989      0.008     13.038      0.000       0.084       0.114
A_MJIND_6             0.1601      0.009     18.329      0.000       0.143       0.177
A_MJIND_7             0.2102      0.012     16.824      0.000       0.186       0.235
A_MJIND_8             0.2219      0.009     25.555      0.000       0.205       0.239
A_MJIND_9             0.1880      0.008     24.314      0.000       0.173       0.203
A_MJIND_10            0.0950      0.007     13.162      0.000       0.081       0.109
A_MJIND_11            0.0378      0.008      4.785      0.000       0.022       0.053
A_MJIND_12            0.0646      0.009      7.045      0.000       0.047       0.083
A_MJIND_13            0.1689      0.009     19.021      0.000       0.151       0.186
A_MJIND_14            0.2501      0.204      1.227      0.220      -0.150       0.650
A_HRLYWK_1           -0.0479      0.004    -11.324      0.000      -0.056      -0.040
A_HRLYWK_2            0.0478      0.005     10.119      0.000       0.039       0.057
WORKYN_2             -0.3816      0.016    -23.700      0.000      -0.413      -0.350
ERN_SRCE_2           -0.7772      0.021    -36.543      0.000      -0.819      -0.736
ERN_SRCE_3           -0.7864      0.056    -13.980      0.000      -0.897      -0.676
ERN_SRCE_4           -0.0739      0.094     -0.784      0.433      -0.259       0.111
CAP_YN_1              0.1392      0.006     22.183      0.000       0.127       0.151
CAP_YN_2              0.0606      0.004     15.905      0.000       0.053       0.068
ED_YN_2               0.1258      0.008     15.544      0.000       0.110       0.142
FIN_YN_2              0.1622      0.015     11.105      0.000       0.134       0.191
CSP_YN_2             -0.0156      0.010     -1.493      0.135      -0.036       0.005
HEA_2                -0.0128      0.003     -3.748      0.000      -0.019      -0.006
HEA_3                -0.0332      0.004     -8.918      0.000      -0.041      -0.026
HEA_4                -0.0722      0.006    -11.730      0.000      -0.084      -0.060
HEA_5                -0.1061      0.013     -7.920      0.000      -0.132      -0.080
A_AGE_A_SEX_2_INT    -0.0013      0.000     -7.118      0.000      -0.002      -0.001
==============================================================================
Omnibus:                    23042.429   Durbin-Watson:                   1.891
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           218043.162
Skew:                          -1.324   Prob(JB):                         0.00
Kurtosis:                      11.264   Cond. No.                     6.31e+05
==============================================================================
```

We should do an F test to check if the coefficients of race dummies(the variable PRDTRACE) are globally significant. 
- The statistic used is F = ((Rsq_nr-Rsq_r)/q)/((1-Rsq_nr)/(n-k-1))
- q: 25
- n-k-1: 69405

The value of the F statistic is 3.256796. and it would be distributed ~F(q;n-k-1)=F(25,69405). We can check in the F probability table for the critical value with 95% confidence.
The critical region is RC={F>=F(25;69405)(0.05)}
The critical value, according to the table is 1.51
This means there is enough statistical evidence to reject the null hypothesis of all coefficients on the PRDTRACE dummies = 0 with 95% confidence.

We can do the same test for the PRCITSHP variable
- F=35.34908 ~ F(4;69405)(0.05) = 2.37
In this case there is enough evidence to reject the null hypothesis of all coefficients on the PRCITSHP dummies = 0 with 95% confidence.

We can see this clearly in the p-values of the model too. There is a clear multicollinearity problem in the model, so it could be creating a bias on the t-statistics and therefore individual p-values. However, joint F-tests show that both PRDTRACE and PRCITSHP dummies contribute significantly to explaining WSAL_VAL_log, so they should be kept in the model despite some individual coefficients appearing insignificant.
There are 26 categories for PRDTRACE, so we can try merging them.

Before doing that, we can calculate the variance inflation factor(VIF) for the independent variables.
According to Wooldridge, we have to run a regression of an independent variable with the rest, and then calculate VIF=(1/(1-Rsquared)), we assume that there could be a multicollinearity problem if this metric is higher than 10.

If we print get_vars_highVIF() we get the following output:
```
VIF FOR const is 1004.3615001653995
VIF FOR A_AGE is 46.4564859163114
VIF FOR A_AGE_SQ is 41.37763591487835
VIF FOR A_HGA_36 is 11.552921971231811
VIF FOR A_HGA_37 is 14.342979145652919
VIF FOR A_HGA_39 is 128.69279518171473
VIF FOR A_HGA_40 is 85.93806912525096
VIF FOR A_HGA_41 is 30.343462560004106
VIF FOR A_HGA_42 is 40.18237147676112
VIF FOR A_HGA_43 is 124.80083289916938
VIF FOR A_HGA_44 is 68.24438173520814
VIF FOR A_HGA_45 is 10.669742253385747
VIF FOR A_HGA_46 is 16.855087548475623
VIF FOR A_AGE_A_SEX_2_INT is 10.479537664093389
['const', 'A_AGE', 'A_AGE_SQ', 'A_HGA_36', 'A_HGA_37', 'A_HGA_39', 'A_HGA_40', 'A_HGA_41', 'A_HGA_42', 'A_HGA_43', 'A_HGA_44', 'A_HGA_45', 'A_HGA_46', 'A_AGE_A_SEX_2_INT']
```
We should merge the A_HGA categories too. We'll simplify them into three: High-school or less, Bachelor's degree, Master's and beyond.
And we will merge PRDTRACE(race) into white and non white. We can also merge A_MARITL into married and not married.

We can further simplify the model by dropping the squared term for age and the interaction of age with sex.

```
                           OLS Regression Results                                   
==============================================================================       
Dep. Variable:           WSAL_VAL_log   R-squared:                       0.417       
Model:                            OLS   Adj. R-squared:                  0.416       
Method:                 Least Squares   F-statistic:                     1181.       
Date:                Fri, 05 Sep 2025   Prob (F-statistic):               0.00       
Time:                        18:31:55   Log-Likelihood:                -29451.       
No. Observations:               69489   AIC:                         5.899e+04       
Df Residuals:                   69446   BIC:                         5.938e+04       
Df Model:                          42                                                
Covariance Type:            nonrobust                                                
=====================================================================================
                        coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------
const                 3.7603      0.022    174.478      0.000       3.718       3.803
A_AGE                 0.0027      0.000     24.262      0.000       0.002       0.003
A_HRS1                0.0083   9.93e-05     83.373      0.000       0.008       0.008
LKWEEKS              -0.0110      0.000    -38.721      0.000      -0.012      -0.010
H_NUMPER             -0.0150      0.001    -15.309      0.000      -0.017      -0.013
A_SEX_2              -0.1017      0.003    -33.123      0.000      -0.108      -0.096
PRDTRACE_merged_1    -0.0063      0.003     -1.825      0.068      -0.013       0.000
PRCITSHP_2           -0.0203      0.020     -1.038      0.299      -0.059       0.018
PRCITSHP_3           -0.0013      0.014     -0.093      0.926      -0.029       0.027
PRCITSHP_4            0.0145      0.005      2.842      0.004       0.005       0.025
PRCITSHP_5           -0.0424      0.005     -8.501      0.000      -0.052      -0.033
A_HGA_merged_1        0.1501      0.003     44.856      0.000       0.144       0.157
A_HGA_merged_2        0.3074      0.005     62.662      0.000       0.298       0.317
A_MARITL_merged_1     0.1258      0.003     38.866      0.000       0.119       0.132
A_HRLYWK_1           -0.0628      0.004    -14.194      0.000      -0.072      -0.054
A_HRLYWK_2            0.0665      0.005     13.458      0.000       0.057       0.076
WORKYN_2             -0.4007      0.017    -23.724      0.000      -0.434      -0.368
ERN_SRCE_2           -0.7752      0.022    -34.738      0.000      -0.819      -0.731
ERN_SRCE_3           -0.7968      0.059    -13.501      0.000      -0.912      -0.681
ERN_SRCE_4           -0.0815      0.099     -0.824      0.410      -0.275       0.112
CAP_YN_1              0.1560      0.007     23.869      0.000       0.143       0.169
CAP_YN_2              0.0690      0.004     17.400      0.000       0.061       0.077
ED_YN_2               0.1721      0.008     20.487      0.000       0.156       0.189
FIN_YN_2              0.1505      0.015      9.824      0.000       0.121       0.181
CSP_YN_2             -0.0761      0.011     -7.008      0.000      -0.097      -0.055
HEA_2                -0.0039      0.004     -1.088      0.277      -0.011       0.003
HEA_3                -0.0266      0.004     -6.828      0.000      -0.034      -0.019
HEA_4                -0.0662      0.006    -10.281      0.000      -0.079      -0.054
HEA_5                -0.0940      0.014     -6.692      0.000      -0.122      -0.066
A_MJIND_1             0.0957      0.015      6.511      0.000       0.067       0.124
A_MJIND_2             0.3077      0.021     14.342      0.000       0.266       0.350
A_MJIND_3             0.2325      0.009     26.226      0.000       0.215       0.250
A_MJIND_4             0.2274      0.008     26.950      0.000       0.211       0.244
A_MJIND_5             0.1169      0.008     14.711      0.000       0.101       0.132
A_MJIND_6             0.1987      0.009     21.750      0.000       0.181       0.217
A_MJIND_7             0.2636      0.013     20.151      0.000       0.238       0.289
A_MJIND_8             0.2695      0.009     29.688      0.000       0.252       0.287
A_MJIND_9             0.2342      0.008     28.975      0.000       0.218       0.250
A_MJIND_10            0.1375      0.008     18.226      0.000       0.123       0.152
A_MJIND_11            0.0224      0.008      2.706      0.007       0.006       0.039
A_MJIND_12            0.0905      0.010      9.415      0.000       0.072       0.109
A_MJIND_13            0.2187      0.009     23.557      0.000       0.201       0.237
A_MJIND_14            0.2908      0.214      1.361      0.174      -0.128       0.710
==============================================================================
Omnibus:                    20849.282   Durbin-Watson:                   1.878
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           158802.698
Skew:                          -1.237   Prob(JB):                         0.00
Kurtosis:                       9.981   Cond. No.                     8.63e+03
==============================================================================
```

In this model, multicollinearity has improved vastly. This can be seen by comparing the condition number, which decreased from 6.31e+05 to 8.63e+03. We can calculate the VIF again for every variable. The condition number seems fine, considering the sample size and that we are mostly working with categorical variables.

```
VIF FOR const is 236.0207191226794
['const']
```
Only the constant has a VIF higher than 10. Most variables present a VIF close to 5 or less.

### Interpretation
- The model is globally significant with 95% confidence, we can see this through the F-statistic=1181 or the p-value.

- It is predicted that an extra hour worked per week is associated on average to a 0.83% higher wage and salary earnings, with 95% confidence.

- Each additional week not worked reduces the wage and salary earnings on average by 1.1% with 95% confidence.

- An extra person living in the household is predicted to reduce the wage and salary earnings on average by 1.5% with 95% confidence.

- It is predicted that women earn on average about 10.2% less than men with 95% confidence, everything else equal.

- Possessing a bachelors degree increases the wage and salary earnings on average by 15%, compared to individuals whose maximum education level is high-school, with 95% confidence.

- Possessing a Master's degree or higher, increases the individual's wage and salary earnings on average by 30.7%, compared to individuals whose maximum education level is high-school, with 95% confidence.

- Salaried workers earn on average 14% more than workers paid by the hour, with 95% confidence.

- It is predicted that being married increases the wage and salary earnings on average by 12.58% compared to not being married, with 95% confidence.

- It is predicted that foreign born(not US citizens) individuals earn on average 4.24% less wage and salary than native US citizens, with 95% confidence.

- Individuals who didn't work at a job or business at any time during 2020, earn on average 40.07% less than the ones who did, with 95% confidence.

- Receiving capital gains from shares of stock or mutual fund are associated on average with 15.6% higher wages than individuals who didn't, with 95% confidence.

- Not receiving educational assistance is associated on average with a 17.2% higher wage and salary than the earned by individuals who did, with 95% confidence.

- Poorer health is associated with lower wage and salary earnings than the ones earned by healthy individuals.

- Manufacturing workers earn about 14% more than agriculture workers. 

- Individuals who work on the mining, quarrying, and oil and gas extraction sectors earn about 24% more than agriculture workers.

- Finance workers earn about 19% more than agriculture workers.

# Sources
- Current Population Survey, 2024 Annual Social and Economic (ASEC) Supplement conducted by the U.S. Census Bureau for the Bureau of Labor Statistics. – Washington: U.S. Census Bureau [producer and distributor], 2024
- Wooldridge, Jeffrey M.(2010) Introductory Econometrics, Fourth Edition








