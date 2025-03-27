clear all
X= csvread('X.csv');
y = csvread('y.csv');

y(y==0) = 10;

X = zscore(X);

X = X(:,1:100)

X = X';
y = y';

[testclass ,accuracy] = ...
  validate(X, y, X,50000)


 

function [testclass ,accuracy] = validate(traindata,trainclass,testdata,maxEpochs)

%classification
[testclass,t,wHidden,wOutput] = mlp_template(traindata,trainclass,testdata,maxEpochs);
trainclass(trainclass==10) = 0;
accuracy = mean(trainclass == testclass);

%plot 
%plotmlp(testdata,testclass,trainclass,wHidden,wOutput);
end


% X = Data;%(:,1:100);
% X = rescale(X);
% %X = abs(X);
% y = Data(:,667);
% 

% n1 = 1;

%csvwrite('X.csv',X);
% csvwrite('y.csv',y);

% n0 = size(X,1);
% n2 = size(y,1);
% [W1,b1,W2,b2] = initialisation(n0,n1,n2);
% % 
% [A1,A2] = model(X,W1,W2,b1,b2);
% % 
% [dW1,db1,dW2,db2] = gradients(X,y,A1,A2,W2);
% 
%[W1,b1,W2,b2] = update(dW1,db1,dW2,db2,W1,W2,b1,b2,0.1);

%[y_test,W2,A2] = neural_network(X,y,n1,0.0001, 5000);

