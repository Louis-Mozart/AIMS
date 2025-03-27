function y_out = NN(x_new,X,y)


y_out = [];
for j = 1:size(x_new,1)
    d = [];
    for i = 1:size(X,1)
        dist = norm(X(i,:)-x_new(j,:));
        d = [d,dist];
        ind = d==min(d);
        y_pred = y(ind);
    end
    y_pred = mode(y_pred);
    y_out = [y_out;y_pred];
end

