Cointegration between real GDP per capita, GHG emissions per capita, Fossil fuel energy consumption and Agriculture, forestry, and fishing, value added in Uruguay between 1984 and 2014, and environmental Kuznets curve analysis.

## Augmented dickey fuller and Johansen cointegration tests
In order to test for stationarity, we use the adfuller function from the statmodels library. By using an iterative process, we can test for a unit root, and if the series is not stationary, we differentiate it and try again until we reject the null hypothesis of stationarity. We can make use of visual tools to check for a constant mean in the series. After repeating this process with all the variables, we reach the conclusion that they are all integrated of order 1, meaning they have to be differentiated once in order to get stationarity. It is necessary that  all the variables have the same order of integration to move forward and test for cointegration.

```
totalghg
ADF statistic           : -5.8497
p-value             : 0.0000

fossil
ADF statistic           : -5.2729
p-value             : 0.0000

agr_va
ADF statistic           : -5.2324
p-value             : 0.0000

realgdp
ADF statistic           : -3.4017
p-value             : 0.0109
 
```

The ADF test has shown that the data meets the criteria to be tested for cointegration, they all have the same integration order.

For the cointegration test, we can use the coint_johansen function from the statsmodels library. The series will be tested on level, not with the differences applied. 
```
Statistic value: [58.20071374 23.23518361  9.97329324  1.4353072 ]
Critical values (95%): [47.8545 29.7961 15.4943  3.8415]
```
The trace statistic is greater than the critical value in this first hypothesis with 95% confidence. Specifically, for the null hypothesis that there are zero cointegrating relationships, the trace statistic value is 58.2007 which is greater than the critical value of 47.8545, meaning we have enough statistical evidence to reject the null hypothesis of zero cointegrating equations in the model at 95% confidence level. The same can't be said for the remaining hypothesis, meaning we can't assure there is more than one cointegrating equation.

The Johansen cointegration test shows that there is a unique cointegration relationship between the variables, meaning that despite the variables being individually non-stationary, there exists one stable, long-term equilibrium relationship among them. In other words, although the variables may fluctuate in the short term, they move together over time in a way that keeps a specific linear combination of them stable.

## Vector Error Correction Model(VECM)
```
Det. terms outside the coint. relation & lagged endog. parameters for equation totalgh
===============================================================================
                  coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------
lin_trend       0.0076      0.002      4.169      0.000       0.004       0.011
L1.totalghg    -0.0209      0.196     -0.106      0.915      -0.405       0.364
L1.fossil       0.0791      0.132      0.597      0.550      -0.180       0.339
L1.agr_va       0.0372      0.046      0.805      0.421      -0.053       0.128
L1.realgdp      0.6242      0.158      3.950      0.000       0.314       0.934
Det. terms outside the coint. relation & lagged endog. parameters for equation fossil
===============================================================================
                  coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------
lin_trend       0.0120      0.004      2.978      0.003       0.004       0.020
L1.totalghg    -0.6072      0.433     -1.401      0.161      -1.457       0.242
L1.fossil       0.6291      0.292      2.151      0.031       0.056       1.202
L1.agr_va       0.1235      0.102      1.207      0.227      -0.077       0.324
L1.realgdp      1.4076      0.349      4.032      0.000       0.723       2.092
Det. terms outside the coint. relation & lagged endog. parameters for equation agr_va
===============================================================================
                  coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------
lin_trend       0.0148      0.006      2.649      0.008       0.004       0.026
L1.totalghg     1.4458      0.598      2.417      0.016       0.273       2.618
L1.fossil      -0.8332      0.404     -2.064      0.039      -1.624      -0.042
L1.agr_va      -0.1842      0.141     -1.305      0.192      -0.461       0.092
L1.realgdp     -0.6995      0.482     -1.452      0.146      -1.644       0.245
Det. terms outside the coint. relation & lagged endog. parameters for equation realgdp
===============================================================================
                  coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------
lin_trend       0.0037      0.002      1.691      0.091      -0.001       0.008
L1.totalghg     0.1218      0.237      0.515      0.607      -0.342       0.586
L1.fossil       0.1193      0.160      0.747      0.455      -0.194       0.432
L1.agr_va      -0.0616      0.056     -1.104      0.270      -0.171       0.048
L1.realgdp      0.5070      0.191      2.660      0.008       0.133       0.881
              Loading coefficients (alpha) for equation totalghg
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
ec1           -0.3173      0.072     -4.417      0.000      -0.458      -0.177
               Loading coefficients (alpha) for equation fossil
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
ec1           -0.5528      0.159     -3.483      0.000      -0.864      -0.242
               Loading coefficients (alpha) for equation agr_va
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
ec1           -0.5911      0.219     -2.699      0.007      -1.020      -0.162
              Loading coefficients (alpha) for equation realgdp
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
ec1           -0.1168      0.087     -1.347      0.178      -0.287       0.053
          Cointegration relations for loading-coefficients-column 1
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
beta.1         1.0000          0          0      0.000       1.000       1.000
beta.2         0.8236      0.187      4.394      0.000       0.456       1.191
beta.3         0.2248      0.067      3.340      0.001       0.093       0.357
beta.4         0.8660      0.091      9.497      0.000       0.687       1.045
==============================================================================
```
The trend coefficient is significant at 95% confidence for all variables except for realgdp, which has a trend coefficient statistically significant at 90%

We can proceed to interpret the short term effects for the fossil variable, its own past persists, a 1% increase of the fossil fuel energy consumption will increase 0.6291% in the next period with a 95% significance. An 1% increase of the real GDP per capita will lead to a positive 1.4076% change in the fossil fuel energy consumption, with a 99% confidence.

For the agr_va variable, a 1% increase of the fossil variable will lead to a reduction of agriculture, forestry, and fishing value added as a percentage of the GDP in -0.8332%. An 1% increase of the real GDP per capita will lead to a positive 1.4458% change in the agriculture, forestry, and fishing value added as a percentage of the GDP, with a 95% confidence.

The real GDP per capita has a positive relationship with its own past, specifically with the previous year's value.

The GHG emission per capita has a positive relationship with the real GDP per capita. A 1% change on the real GDP per capita will lead to a positive increase of 0.6242% in the GHG emissions per capita with 99% confidence.

When we analyze the error correction coefficient, that is, the long term adjustment, fossil, agr_va and totalghg actively participate in the long term adjustment mechanism, however realgdp coefficient has p-value of 0.178. All the β coefficients are positive and highly significant with p-values lower than 0.01. This could indicate a stable long term relationship between fossil, agr_va, realgdpd and totalghg.

#### Interpretation of the results
There is a clear positive relationship with the shocks from real GDP per capita and the fossil fuel energy consumption, however, this relationship is not clear in the reverse order, this means an increase in the usage of fossil fuel as energy doesn't necessarily increase GDP per capita, but as the economy grows, there is an increasing need for energy consumption, and in this period, agents use more of this energy source to satisfy this need. In the long term this relationship is negative, this might be because of the structural change on the energy sources in the production system.

It could indicate an increase of urbanization and usage of vehicles, as the individuals get more income, they can afford to import personal vehicles, and businesses adopt vehicles to increase efficiency, more data would be needed to analyze this hypothesis.

The usage of a trend made sense, as most of the variables had significant trends in the short term.

The agr_var increases as the GHG emissions per capita increase, this might be due to the environmental pollution of livestock and agriculture, plus the destruction of biodiversity and inefficient production techniques. We must remember the production matrix of Uruguay is mostly composed of commodities and it's a big exportator of products such as meat. 

The GHG emissions per capita are impacted positively by real GDP per capita and Fossil fuel energy consumption in the short term. This makes sense and it's the expected relationship. The higher the production, the higher the energy consumption from environmentally harmful sources and the higher the GHG emissions, even though the fossil coefficient wasn't statistically significant.

This model shows a partial transition from the usage of fossil fuel energy consumption and its impact on emissions, as we discussed earlier, this happened due to the adoption of alternative energy sources. The agriculture and livestock sector doesn't seem to have a statistically strong impact over other variables on the short term.

We can analyze the long term with the following equation(that is, the cointegration relations).

$$totalghg=0.8236agrva+0.2248realgdp+0.8660fossil​+error$$

The fossil variable has the highest coefficient with the value 0.8660, this means fossil fuel energy consumption is the lead cause of emissions in the long term and should be regulated. In respect to the agr_va variable, while I couldn't analyze the model with more than one lag, and no statistically significant evidence of its impact over GHG emissions per capita was found on the short term, there is a clear positive effect over the emissions on the long term. Interestingly, real GDP per capita has the least impact of the three variables, this might be explained by the lack of an industrial sector in the country. All the coefficients are positive and highly statistically significant.

## Impulse response functions(IRF)
![VECM_90confidence](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeYGSZ3jkH8KyCXCrsBpj_WbTOcUmRM3fNTGFXjjKmcaNrNkTmXgI6t75H-eg9fUBpkH4PY9K6nDb4hZAQfuc9NRW8-dznE6JePebVSENOOp99uCGl5nP1f6CymzcwcEHKOLtgL9Q?key=ASHQOkzP-YpF5MYx9TD1xA)

Let's analyze the most important relationships. An unexpected positive shock on the real GDP per capita impacts positively on GHG emissions per capita(totalghg), this shock then impacts negatively after the second period, then, the shock remains with its negative impact over time, as it can be seen with the confidence interval bounds, the shock doesn't converge to zero. The shock behaves similarly over the fossil fuel energy consumption, but unlike with the other variable, the shock dies over time.

Shocks on the GDP per capita impact negatively on the non industrial sector, represented in this model by the agriculture and livestock variable. This might be caused by the transition to a service economy and urbanization.

Another interesting relationship is the impact on the Agriculture and livestock over fossil consumption, it impacts negatively until the second year, when the shock impact is reversed and then dies. The rural sector may initially be forced to reduce fossil use due to adoption of renewable energy, efficient machinery, or low-energy practices. Unlike the industrial sector, agriculture is labour rather than energy intensive, which may explain the initial negative behaviour, later, rural businesses' need for fossil fuel energy use could be explained by seasonality, there are long periods in which crop production or animal growth don't make use of this kind of energy.

Lastly, GHG emissions per capita shocks will have an immediate positive impact over fossil fuel energy consumption. This is expected as fossil fuel combustion is a major source of GHGs, and if the initial shock is explained by economic growth, it would make sense that the agents would need to increase energy consumption to satisfy the higher production, implying there is not yet a complete transition to renewable energy sources.

## Environmental Kuznets curve
The environmental Kuznets curve (EKC) is a hypothesis about the relationship between pollution and economic development. The environmental problems get worse as the economy grows, but after a certain turning point, where the average income is high enough, the relationship is reversed. So, "the solution to pollution is economic growth.". Despite the critics, this is a known phenomenon, emissions increase with GDP up to a point, then decrease.

For the following analysis we can create  a new variable: the square of the logarithm of real GDP per capita, and then run an ADF to be sure it is integrated of order 1, the first difference having a p-value of 0.0123, rejecting the null hypothesis. Then we run Johansen's cointegration test, but only with the GHG emissions per capita, real GDP per capita and its quadratic form.

From the test, the trace statistic value is 43.29 and the critical value at 95% confidence is 29.79, therefore we can reject the null hypothesis of zero cointegration equations, meaning there is at least one cointegration relationship, but there is not enough statistical evidence of more than one.

The next step is running the VECM and checking the following equation:

$$ \log(totalghg) = \beta_1 \log(totalghg) + \beta_2 \log(realgdp) + \beta_3 \log(realgdp)^2 + error $$

If we get β2>0 and then β3<0 we find evidence of the environmental Kuznets curve in Uruguay between 1984 and 2014, which is as we discussed earlier, a period in which Uruguay transitioned to a services economy. With a confidence of 99%, we can say 

$$ \beta_2=2.3206>0 \text{ and }$$
$$ \beta_3=−0.1158<0 $$

We can maximize this function and get the turning point, that is, the point in which higher economic growth implies lower pollution. 
In this case:

$$\frac{dlog(totalghg)}{dlog(realgdp)} = \beta_2 + 2\beta_3*log(realgdp) = 0$$

Therefore the turning point is:

$$ \log(realgdp) = \frac{-\beta_2}{2\beta_3} = \frac{-2.3206}{2 \cdot (-0.1158)} = 10.019 $$

Because the variable is in logarithms, we apply an exponential expression to get the value.

$$\text{Turning point} = e^{10.019} \approx 22{,}448.96$$

Therefore the real GDP per capita would be approximately US$22,448.96.

The results of the VECM model is that emissions increase with economic growth until reaching a turning point, estimated at approximately US$22,448.96 (GDP per capita in constant 2015 prices). Beyond this income level, emissions will begin to decline, explained by shifts in the energy source usage toward renewable alternatives, and environmental policies implemented in the country. We can visualize this curve and conclude that during this period Uruguay has not crossed the turning point in the period, which makes sense when we analyze the sign of the coefficient. Analyzing the real gdp per capita time series, Uruguay has crossed the turning point only shortly after 2020.

<img width="1920" height="975" alt="ekcfigure" src="https://github.com/user-attachments/assets/f8ed10d1-8d5e-493c-812a-5a8821db2501" />

## Conclusion
There is strong statistical evidence that Uruguay’s greenhouse gas emissions, fossil fuel energy use, agricultural sector output, and real GDP per capita share a long-term equilibrium relationship, despite their short-term fluctuations. The Johansen cointegration test confirms the existence of a unique cointegrating equation among the variables, allowing the use of a vector error correction model to explore both short and long term dynamics. The error correction model results reveal that fossil fuel consumption has the strongest long-term effect on GHG emissions, followed by agriculture, with real GDP per capita having the smallest but still positive influence. The error correction term suggests that the system adjusts toward long run equilibrium after shocks, with emissions, fossil use, and agriculture significantly participating in the adjustment process. Importantly, real GDP per capita is not statistically significant in the adjustment mechanism, indicating that economic growth alone does not immediately correct imbalances in the environmental system.

The turning point given this data is estimated at around US$22,449 per capita, after which further growth is expected to reduce emissions. This value would change if we take more recent data.

## Data
- Fossil fuel energy consumption (% of total) https://data360.worldbank.org/en/indicator/WB_ESG_EG_USE_COMM_FO_ZS?utm_source=chatgpt.com
- Total population https://data360.worldbank.org/en/indicator/WB_WDI_SP_POP_TOTL
- Agriculture, forestry, and fishing, value added (% of GDP) API_NV.AGR.TOTL.ZS_DS2_en_csv_v2_21645 https://data.worldbank.org/indicator/NV.AGR.TOTL.ZS
- GDP (constant 2015 US$) - Uruguay https://data.worldbank.org/indicator/NY.GDP.MKTP.KD?locations=UY
- Total greenhouse gas emissions excluding LULUCF (Mt CO2e) https://data.worldbank.org/indicator/EN.GHG.ALL.MT.CE.AR5

## Requirements
Install the required packages with the following command:
`pip install statsmodels seaborn matplotlib pandas numpy`

