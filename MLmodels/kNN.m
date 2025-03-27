function y_out = kNN(x_new,X,y,k)

y_out = [];
for j = 1:size(x_new,1)
    d = [];
    for i = 1:size(X,1)
        dist = norm(X(i,:)-x_new(j,:));
        d = [d,dist];
    end
    [~,ind] = sort(d);
    indk = ind(1:k);
    y_pred = y(indk);
    y_pred = mode(y_pred);
    y_out = [y_out;y_pred];
end

% function c = tiebreak(y,indk,i,k,p)
% 
% Z = zeros(10,1000);
% h = trainclass(indk,i);
% 
% for j = 1:k
% 
%     if h(j) == 1
%         z(1)