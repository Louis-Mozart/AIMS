function [A1,A2] = model(X,W1,W2,b1,b2)

       Z1 = W1*X+b1;
       %Z1 = rescale(Z1);
       A1 = (1+exp(-Z1)).^(-1);
       %A  = tanh(Z);
       %A = A';
       
       Z2 = W2*A1+b2;
       %Z2 = rescale(Z2);
       %A2 = (1+exp(-Z2)).^(-1);
       A2 = tanh(Z2);

end