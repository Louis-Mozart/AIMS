clear all
X = csvread('X.csv');
y = csvread('y.csv');
X = sparse(X); 

Data = [X y];

x = linspace(0,1,100);
i = 0 % counter to see the progression of the for loop
acc = []; % empty vector to contain the accuracy of each sample

for k = 1:100
    [X_train,y_train,X_test,y_test] = split_data(Data,0.9); %splitting the data with 100 samples in the test and 900 in the training

    x_new = X_test;

    y_pred = kNN(x_new,X_train,y_train,1); %prediction
    
    ac =  mean(y_pred == y_test); % compute the accuracy
    acc = [acc, ac]; % saving the accuracy
    i = i+1
end 

m = mean(acc); % compute the mean accuracy

% plot the accuracy 

figure(1)
plot(x,acc,'-b'), hold on
yline(m,'--r',LineWidth=2),hold off
legend('accuracy','mean accuracy')
axis([0 1 .75 .95 ])
label = 0:9;

c = confusionmat(y_test,y_pred);

% plot the confusion matrix

figure(2)

% generate the confusion matrix

confusionchart(c,label)



disp(mean(acc));

