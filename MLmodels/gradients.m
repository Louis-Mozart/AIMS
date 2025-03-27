function [dW1,db1,dW2,db2] = gradients(X,y,A1,A2,W2)

% m = length(y);
% 
% dw = 1/m*X'*(A-y);
% db = 1/m*sum(A-y);

m = length(y);
dZ2 = A2-y;
dW2 = 1/m * dZ2*A1';
db2 = 1/m * sum(dZ2,2);

dZ1 = W2'*dZ2.*A1.*(1-A1);
dW1 = 1/m*dZ1*X';
db1 = 1/m*sum(dZ1,2);

end
