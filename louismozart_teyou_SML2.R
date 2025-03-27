library(readr)
library(class)
library(MASS)
library(kernlab)
library(mlbench)
library(reshape2)
library(ROCR)
library(ggplot2)

library(xtable)

# Exercice 3

mnist_train <- read_csv("https://pjreddie.com/media/files/mnist_train.csv", col_names = FALSE)
ssss# 
smnist_test <- read_csv("https://pjreddie.com/media/files/mnist_test.csv", col_names = FALSE)
# 



# Exercice 4


prostate <- read.csv("prostate-cancer-1.csv") 

#1 building the four learning machine:

 
x   <- prostate[,-1]      # Data matrix: n x p matrix
y   <- prostate[, 1]      # Response vector
                                    


k <- 1
y_train_hat <- knn(x, x,y, k=k) # Predicted responses in test set

conf.mat.tr <- table(y, y_train_hat)
xtable(conf.mat.tr)
conf.mat.tr

k <- 3 
y_train_hat <- knn(x, x,y, k=k)
conf.mat.tr <- table(y, y_train_hat)
conf.mat.tr
xtable(conf.mat.tr)

k <- 5
y_train_hat <- knn(x, x,y, k=k)
conf.mat.tr <- table(y, y_train_hat)
conf.mat.tr
xtable(conf.mat.tr)

k <- 7
y_train_hat <- knn(x, x,y, k=k)
conf.mat.tr <- table(y, y_train_hat)
conf.mat.tr
xtable(conf.mat.tr)

n <- nrow(prostate)

id.tr   <- sample(sample(sample(n)))[1:n]   # For a sample of ntr indices from {1,2,..,n}
#id .tr <- sample(1:n, ntr, replace=F)        # Another way to draw from {1,2,..n}
id.te   <-sample(sample(sample(n)))[1:n]
id.te
id.tr

y.roc <- ifelse(y=='pos',1,0)

y.roc <- ifelse(y=='pos',1,0)

kNN.mod <- class::knn(x[id.tr,], x[id.tr,], y, k=1, prob=TRUE)
prob    <- attr(kNN.mod, 'prob')
prob    <- 2*ifelse(kNN.mod == "0", 1-prob, prob) - 1

pred.1NN <- prediction(prob, y)
perf.1NN <- performance(pred.1NN, measure='tpr', x.measure='fpr')

kNN.mod <- class::knn(x[id.tr,], x[id.tr,], y, k=3, prob=TRUE)
prob    <- attr(kNN.mod, 'prob')
prob    <- 2*ifelse(kNN.mod == "0", 1-prob, prob) - 1

pred.3NN <- prediction(prob, y)
perf.3NN <- performance(pred.3NN, measure='tpr', x.measure='fpr')

kNN.mod <- class::knn(x[id.tr,], x[id.tr,], y, k=5, prob=TRUE)
prob    <- attr(kNN.mod, 'prob')
prob    <- 2*ifelse(kNN.mod == "0", 1-prob, prob) - 1

pred.5NN <- prediction(prob, y)
perf.5NN <- performance(pred.5NN, measure='tpr', x.measure='fpr')

kNN.mod <- class::knn(x[id.tr,], x[id.tr,], y, k=7, prob=TRUE)
prob    <- attr(kNN.mod, 'prob')
prob    <- 2*ifelse(kNN.mod == "0", 1-prob, prob) - 1

pred.7NN <- prediction(prob, y)
perf.7NN <- performance(pred.7NN, measure='tpr', x.measure='fpr')

plot(perf.1NN, col=2, lwd= 2, lty=2, main=paste('Comparison of Predictive ROC curves'))
plot(perf.3NN, col=3, lwd= 2, lty=3, add=TRUE)
plot(perf.5NN, col=4, lwd= 2, lty=4, add=TRUE)
plot(perf.7NN, col=5, lwd= 2, lty=5, add=TRUE)
abline(a=0,b=1)
legend('bottomright', inset=0.05, c('1NN','3NN','5NN', '7NN'),  col=2:5, lty=2:5)



set.seed (19671210)          # Set seed for random number generation to be reproducible

epsilon <- 1/3               # Proportion of observations in the test set
nte     <- round(n*epsilon)  # Number of observations in the test set
ntr     <- n - nte

R <- 100   # Number of replications
test.err <- matrix(0, nrow=R, ncol=4)

for(r in 1:R)
{
  # Split the data
  
  id.tr   <- sample(sample(sample(n)))[1:ntr]                   # For a sample of ntr indices from {1,2,..,n}
  id.te   <- setdiff(1:n, id.tr)
  
  y.te         <- y[id.te]                                        # True responses in test set
  
  # First machine: 1NN
  
  y.te.hat     <- knn(x[id.tr,], x[id.te,], y[id.tr], k=1)        # Predicted responses in test set
  ind.err.te   <- ifelse(y.te!=y.te.hat,1,0)                      # Random variable tracking error. Indicator
  test.err[r,1]  <- mean(ind.err.te)
  
  # Second machine: Our optimal NN found earlier with k=k.opt.cv
  y.te.hat     <- knn(x[id.tr,], x[id.te,], y[id.tr], k=3) # Predicted responses in test set
  ind.err.te   <- ifelse(y.te!=y.te.hat,1,0)                      # Random variable tracking error. Indicator
  test.err[r,2]  <- mean(ind.err.te)
  
  # Third machine: k=round(sqrt(n))
  y.te.hat     <- knn(x[id.tr,], x[id.te,], y[id.tr], k=5)       # Predicted responses in test set
  ind.err.te   <- ifelse(y.te!=y.te.hat,1,0)                      # Random variable tracking error. Indicator
  test.err[r,3]  <- mean(ind.err.te)
  
  
  # Fourth machine: k=round(log(n))
  y.te.hat     <- knn(x[id.tr,], x[id.te,], y[id.tr], k=7)       # Predicted responses in test set
  ind.err.te   <- ifelse(y.te!=y.te.hat,1,0)                      # Random variable tracking error. Indicator
  test.err[r,4]  <- mean(ind.err.te)
  
}  

test <- data.frame(test.err)
Method<-c('1NN', '3NN', '5NN', '7NN')
colnames(test) <- Method
boxplot(test)
```  

Once again, we also produce a nicer looking version of the same plot using the
famous ggplot

```{R}
require(reshape2)
ggplot(data = melt(test), aes(x=variable, y=value)) + geom_boxplot(aes(fill=variable))+
  labs(x='Learning Machine', y=expression(hat(R)[te](kNN)))+
  theme(legend.position="none") 




















