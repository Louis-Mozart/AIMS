function [X_train,y_train,X_test,y_test] = split_data(Data,ratio)

%Data = [X,y];


[m,n] = size(Data);
Data = datasample(Data,m);

l = m*ratio;

X = Data(:,1:n-1);
y = Data(:,n);

X_train = X(1:l,:);
X_test = X(l+1:end,:);

y_train = y(1:l,:);
y_test = y(l+1:end,:);

end
