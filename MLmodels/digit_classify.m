function c = digit_classify(data)

%%%%%%%%%%%%%%%% Part1: preprocessing of the input data %%%%%%%%%%%%%%%%%%%%%%%

X= csvread('X.csv');  %training data
y = csvread('y.csv'); %training class
X = sparse(X);        % Sparse the matrix to remove all the zeros and gain space on the memory.

data = zscore(data); % scalling the data
[~,data,~,~,~] = pca(data,'NumComponents',2); %perform pca to get the two principal components of the data
data = data(:);       
L_max = size(X,2);        %Maximum length in the train data
l = length(data);

if l>L_max           %If the length of the guess is greater than L_max, then cut it to 666

   data = data(1:L_max,:);

else                % If not complete it to L_max by adding zeros

    data = padarray(data ,L_max - l , 'post');

end

data = data';      % traspose the data to get a row vector

%%%%%%%%%%%%%%% part2: performing the classification %%%%%%%%%%%%%%

c = ZNN(data,X,y,1); %KNN with 1 neighbors

%%%%%%%%%%%%% part3: function for classification (KNN) %%%%%%%%%%%%%%%%%%

function y_out = ZNN(x_new,X,y,k)

y_out = [];  % this vector will contain the corresponding class for 
             % each row in the test data

%%%%% this first loop will go over all the rows of the guess data
for j = 1:size(x_new,1)

    d = [];   % empty vector that will contain all the distances 
     
    %%%%% This second loop will go over all the rows of the train data
    %%%%% and then compute the L2 distance between the each rows of the 
    %%%%% test data and all the rows in the train data.

    for i = 1:size(X,1)
        dist = norm(X(i,:)-x_new(j,:)); %distance calculation 
        d = [d,dist];   % store the distance into the empty vector
    end

    % sort the distance into ascending order but taking  only
    % the indeces of those minimum distances.

    [~,ind] = sort(d);  
                     
    indk = ind(1:k); % taking k of those indeces 
    y_pred = y(indk); % choose those indeces in the trainclass
    y_pred = mode(y_pred); % taking the class that appear the most.
    y_out = [y_out;y_pred]; % filling the empty vector with the correspondant class.
end

end

end

