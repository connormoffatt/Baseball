# Follow tutorial given at the follwoing website

# Linear Mixed Effects Modeling Using R

# https://it.unt.edu/sites/default/files/linearmixedmodels_jds_dec2010.pdf

# Data Retrived from:
# http://bayes.acs.unt.edu:8083/BayesContent/class/Jon/R_SC/Module9/lmm.data.txt

# Using lme4 package. Linear Mixed Effects version 4
# install.packages("lme4")
# https://cran.r-project.org/web/packages/lme4/lme4.pdf

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Modeling"
setwd(chapter_path)

# Read in the Example Data
library(lme4)
library(arm) # convenience functions for regression in R

lmm.data <- read.table("lmm.data.txt",
                       header=TRUE, sep=",", na.strings="NA", dec=".",
                       strip.white=TRUE)

# The variable extroversion is predicted by fixed effects for the interval
# scaled predictor Openness to new experiences, Agreeableness, social
# enagement, Class, Class within School. Data contains 1200 cases evenly 
# distributed among 24 nested groups (4 classes within 6 schools)

summary(lmm.data)
head(lmm.data)

# Fit the model using the lmer function

# The formula (from left to right) begins with the outcome variable then the
# tilde, followed by all the predictors. The first five predictors represent
# fixed effects and then, in parentheses each random effect is 
# listed. The random effect specifies the nested effect of class within 
# (or under) school; as class would be considered the level one variable and
# school the level two variable - which is why the forward slash is used.

# By default, the lmer function will also model the random effect for the
# highest level variable (school) of th enesting. A standard interaction term
# can be specified using hte colon, for example (1|school:class) would
# specify a random effect (the parenthesis) for the interaction of the school
# and class (the colon)


lmm.2 <- lmer(formula = extro ~ open + agree + social + class + 
                (1|school/class), data = lmm.data)
summary(lmm.2)

# Interpreting the default summary output

# Three values shown for random effects in the form of variances and std. dev.
# If we add the variance components. then we can divide by our nested 
# effect variance  to give us the proportion of variance accounted for,
# which indicates whether or not this is meaningful
2.88 + 95.17 + 0.97
2.88 / 99.02

# Only 2.9% of the total variance of the random effects is attributed to the
# nested effect. If all the percentages for each random effect are very small
# then the random effects are not present and the linear mixed model is not
# appropriate. We can see the effect of the school alone is quite substantial
99.17 / 99.02

# Another way to think about these variance components is in terms used with
# standard ANOVA (Analysis of Variance). The residual variance estimate can be
# thought of as the within groups variance and each random effect variance
# estiamte can be thought of as a between groups estiamte

# Fixed effects estimates are interpreted the same way as one would interpret
# estiamtes from a traditional ordinary least squares linear regression

# Last part is correlation matrix

# Extract estimates of the fixed effects
fixef(lmm.2)

# Extract estimates of random effects
ranef(lmm.2)

# Extract coefficients for the random effects intercept and each group of the 
# random effect factor
coef(lmm.2)

# Extracted fitted or predicted values based on model parameters and ata
yhat <- fitted(lmm.2)
summary(yhat)

# Extract residuals and summarize them
residuals <- resid(lmm.2)
summary(residuals)
hist(residuals)

# ICC (Intra Class Correlation) represents a measure of reliability, or
# dependence among individuals. Allows us to assess whether or not the random
# effect is present in the data. First create a null model; which for the 
# current example would include just the intercepts and the random effect for
# the highest level variable of the nested structure
lmm.null <- lmer(extro ~ 1 + (1|school), data = lmm.data)
summary(lmm.null)

# Next, add the random effect variance estimates and divide the random effect
# of school's variance estimate by the total variance estiamte
95.87 / (95.87 + 7.14)

# We see that the ICC is 0.9306
# Another way to get ICC is with the multilevel package
aov.1 <- aov(extro ~ school, lmm.data)
summary(aov.1)
library(multilevel)
ICC1(aov.1)

# ICC1 indicates that 93.07% of the variance in extro can be explained by school
# group memebership

# We can also get the ICC2, which is a measure of reliability
ICC2(aov.1)

# This high value indicates that school groups can be very reliably differentiated
# in terms of 'extro' scores
detach("package:multilevel")

# Using function mcmcsamp

# MCMC methods represent a type of briddge between traditional frequentist
# methods and Bayesian methods

# MCMC methods use prior information to provide initial parameter estaimtes in 
# order to evaluate subsequent iteratively re-modeled parameter estiamtes

# To obtain a simulated empirical distribution or posterior distribution
# of estiamtes based on specified lmer model using MCMC methods
# This function is no longer a part of lme4:()
mcmc.5000 <- mcmcsamp(lmm.2, saveb=TRUE, n=5000)

#There are other packages for mixed effect modeling. HGLMMM, MCMCglmm, multilevel
