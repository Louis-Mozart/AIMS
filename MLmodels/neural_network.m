function [W2,A2] = neural_network(X,y,n1,alpha, n_iter)

n0 = size(X,1);
n2 = size(y,1);
[W1,b1,W2,b2] = initialisation(n0,n1,n2);

loss = [];
for i = 1:n_iter

    [A1,A2] = model(X,W1,W2,b1,b2);
    %loss = log_loss(A,y);
    loss = [loss log_loss(A2,y)];
    [dW1,db1,dW2,db2] = gradients(X,y,A1,A2,W2);
    [W1,b1,W2,b2] = update(dW1,db1,dW2,db2,W1,W2,b1,b2,alpha);

end
%y_test =  W2.*A2+b2;
plot(loss)
end

