function loss = log_loss(A,y)

%loss = -1/length(y)*sum(y*log10(A+eps)) + (1-y)*log10(1-A+eps);
loss = norm(A-y,2);
% loss = log10(loss);
end