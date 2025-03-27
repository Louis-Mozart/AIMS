clear all

%%%% this codes is to show how we preprocess the training data %%%%%

% reading all the files from their path to the work directory

Folder_0 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\0';
FileList_0 = dir(Folder_0);
matData_0 = [];

for k = 3:numel(FileList_0)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_0(k).folder, FileList_0(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_0 = [matData_0 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end
Folder_1 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\1';
FileList_1 = dir(Folder_1);
matData_1 = [];
for k = 3:numel(FileList_1)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_1(k).folder, FileList_1(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_1 = [matData_1 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_2 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\2';
FileList_2 = dir(Folder_2);
matData_2 = [];
for k = 3:numel(FileList_2)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_2(k).folder, FileList_2(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_2 = [matData_2 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_3 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\3';
FileList_3 = dir(Folder_3);
matData_3 = [];
for k = 3:numel(FileList_3)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_3(k).folder, FileList_3(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_3 = [matData_3 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_4 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\4';
FileList_4 = dir(Folder_4);
matData_4 = [];
for k = 3:numel(FileList_4)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_4(k).folder, FileList_4(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_4 = [matData_4 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_5 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\5';
FileList_5 = dir(Folder_5);
matData_5 = [];
for k = 3:numel(FileList_5)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_5(k).folder, FileList_5(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_5 = [matData_5 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_6 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\6';
FileList_6 = dir(Folder_6);
matData_6 = [];
for k = 3:numel(FileList_6)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_6(k).folder, FileList_6(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_6 = [matData_6 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_7 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\7';
FileList_7 = dir(Folder_7);
matData_7 = [];
for k = 3:numel(FileList_7)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_7(k).folder, FileList_7(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_7 = [matData_7 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_8 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\8';
FileList_8 = dir(Folder_8);
matData_8 = [];
for k = 3:numel(FileList_8)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_8(k).folder, FileList_8(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_8 = [matData_8 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

Folder_9 = 'C:\Users\hp\OneDrive - LUT University\Bureau\PRML\Pratical assignement\digits_3d\training_data\9';
FileList_9 = dir(Folder_9);
matData_9 = [];
for k = 3:numel(FileList_9)
	% OPTION 1: Create a mat filename, and load it into a structure called matData.
	matFileName = fullfile(FileList_9(k).folder, FileList_9(k).name); %sprintf('mat%d.mat', k);
	if isfile(matFileName)
		matData_9 = [matData_9 load(matFileName)];
	else
		fprintf('File %s does not exist.\n', matFileName);
    end
end

% create a structure that will contain all the samples for each digits

X = [matData_0;matData_1;matData_2;matData_3;matData_4;matData_5;matData_6;matData_7;matData_8;matData_9];


%%%%%%%% I want to create the data (a big matrix containing the samples in an horizontal form) %%%%%%

% 1) looking for the maximal length in the data

L = [];
%data  = 
for i = 1:10
    for j = 1:100
        Zij = X(i,j).pos;
        Zij = zscore(Zij);
        [~,Zij,~,~,~] = pca(Zij,'NumComponents',2);
        Zij = Zij(:);
        %l = length(Zij);
        [l ~] = size(Zij);
        L = [l L];
    end
end
disp(max(L));
disp(min(L));
L_max = max(L);

%2 trying to create a shape of the data

Data = [];

for i = 1:10
    data = zeros(100,L_max);
    
    for j = 1:100
        Zij = X(i,j).pos;
        Zij = zscore(Zij);
        [~,Zij,~,~,~] = pca(Zij,'NumComponents',2);
        Zij = Zij(:);
        
    
        l = length(Zij);
    
        Zij = padarray(Zij ,L_max - l , 'post');
        Zij = Zij';
        data(j,:) = Zij;
    end
    Data =  [Data;data];
end  

%%%%%%% Data ready. Now let's go with the response variable: %%%%%%%%%%%%%%%%%%%%%%%%%

y = [zeros(100,1); ones(100,1);2*ones(100,1);3*ones(100,1);4*ones(100,1);5*ones(100,1);6*ones(100,1);7*ones(100,1);8*ones(100,1);9*ones(100,1)];

csvwrite('X.csv',Data); % save the train data 
csvwrite('y.csv',y);    % save the train class

