function accuracy = validate(traindata,trainclass,testdata,C)

%classify the data
testclass = svm2(traindata,trainclass,traindata,C);

%Calculate accuracy
accuracy = mean(trainclass == testclass);

%Data range
mind = min(traindata, [], 2);
maxd = max(traindata, [], 2);
dRange = maxd-mind;

%Grid for features space
[X,Y] = meshgrid(mind(1):.2:maxd(1), mind(2):.2:maxd(2));
D = [X(:) Y(:)]';

%train with data and classify the feature space points
d = svm2(traindata,trainclass,D,C);

%Visualisation
figure()
d(d==-1) = 2;

%decision regions

plot(D(1,d==1),D(2,d==1),'g.',D(1,d==2),D(2,d==2),'y.');
hold on;

%data points

plot(testdata(1,testclass==1),testdata(2,testclass==1),'bo',testdata(1,testclass==2),testdata(2,testclass==2),'ro');
hold off;

legend('class1','class2');
axis([mind(1)-0.15*dRange(1),maxd(1)+0.15*dRange(1),mind(2)-0.15*dRange(2),maxd(2)+0.15*dRange(2)]);
drawnow;

end


