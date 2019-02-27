# Follow tutorial given at the follwoing website
# https://www.jaredknowles.com/journal/2013/11/25/getting-started-with-mixed-effect-models-in-r

# https://it.unt.edu/sites/default/files/linearmixedmodels_jds_dec2010.pdf

# Getting Started with Mixed Effect Models in R

# Data Retrived from:
# http://bayes.acs.unt.edu:8083/BayesContent/class/Jon/R_SC/Module9/lmm.data.txt

# Using lme4 package
# install.packages("lme4")

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Modeling"
setwd(chapter_path)

# Read in the Data
library(lme4)
library(arm) # convenience functions for regression in R

lmm.data <- read.table("lmm.data.txt",
                       header=TRUE, sep=",", na.strings="NA", dec=".",
                       strip.white=TRUE)

# Fit hte non-multilevel models
# Fit a simple OLS regerssion of measures of openness, agreeableness, and
# sociability on extroversion. We use display from arm for abbreviated output
OLSexamp <- lm(extro ~ open + agree + social, data = lmm.data)
display(OLSexamp)

# This model does not fit very well. R model interface is quite simple

# If we want to extract measures such as the AIC, we may prefer to fit a 
# generalized linear model with glm which produces a model fit through
# maximum likelihood estimation. Note that the model formula specification is
# the same
MLexamp <- glm(extro ~ open + agree + social, data=lmm.data)
display(MLexamp)
AIC(MLexamp)

# This results in a poor model

# Fit a varying intercept model. Using a grouping variable such as school or
# class. Varying interceptmodel just means we add a categorical variable to 
# adjust the intercept
MLexamp.2 <- glm(extro ~ open + agree + social + class, data = lmm.data)
display(MLexamp.2)
AIC(MLexamp.2)
anova(MLexamp, MLexamp.2, test = "F")

# This is a fixed effects specification often. This is simply the case of 
# fitting a separate dummy variable as a predictor for each class. We can see
# that this does not provide much additional model fit

# Let us see if school is any better
MLexamp.3 <- glm(extro ~ open + agree + social + school, data=lmm.data)
display(MLexamp.3)
AIC(MLexamp.3)
anova(MLexamp, MLexamp.3, test="F")

# The school effect greatly improves our model fit. However, how do we interpret
# these effects
table(lmm.data$school, lmm.data$class)

# here we can see we have a perfectly balanced design with 50 observations in 
# each combination of class and school

# Let's try to model each of these unique cells. To do this we fit a model and 
# use the : operator to specify interaction between school and class
MLexamp.4 <- glm(extro ~ open + agree + social + school:class, data = lmm.data)
display(MLexamp.4)
AIC(MLexamp.4)

# This is very useful, but what if we want to understand both the effect of the
# scdhool and the effect of the class, as well as the effect of the schools and
# classes? Unfortunately this is not easily done with standard glm
MLexamp.5 <- glm(extro ~ open + agree + social + school * class - 1, 
                 data=lmm.data)
display(MLexamp.5)
AIC(MLexamp.5)

# Exploring Random Slopes
# another alternative is to fit a separate model for each of the school and
# class combinations. If we believe the relationship between our variabels
# may be highly dependent on the school and class combination, we can simply
# fit a series of models and explore the parameter variation among them
require(plyr)
modellist <- dlply(lmm.data, .(school, class), function(x) glm(extro ~ open +
                   agree + social, data = x))
display(modellist[[1]])
display(modellist[[2]])

# Fit a varying intercept model with lmer
# While all of the above techniques are valid approaches to this problem, they
# are not necessarily the best approach when we are interested explicitly in 
# variation among and by groups. This is where a mixed-effect modeling framework
# is useful. Now we use the lmer function witht eh familiar formula interface
# but now group level variables are specified using a special syntax (1|school)
# tells lmer to fit a lienar model witha  varying intercept group using the
# variable school
MLexamp.6 <- lmer(extro ~ open + agree + social + (1| school), data=lmm.data)
display(MLexamp.6)

# We can fit multiple group effects with multiple group effect terms
MLexamp.7 <- lmer(extro ~ open + agree + social + (1| school) + (1|class),
                  data=lmm.data)

# finally we ca fit nested group effect terms through the following syntax.
# Here the (1|school/class) says that we want to fit a mixed effect erm for
# varying itercepts 1|by schools, and for classes that are nested within schools
MLexamp.8 <- lmer(extro ~ open + agree + social + (1| school/class), 
                  data=lmm.data)
display(MLexamp.8)

# Fita  varying slope model with lmer. Instead of fitting unique models by school,
# we can fit a varying slope model. Here we modify our random effect term to
# include variables before the grouping terms: (1 + open|school/class) tells
# R to fit a varying slope and varying intercept model for schools and classes
# nested within schools, and to allow the slope of the open variable to vary
# by school
MLexamp.9 <- lmer(extro ~ open + agree + social + (1 + open | school/class),
                  data=lmm.data)
display(MLexamp.9)
