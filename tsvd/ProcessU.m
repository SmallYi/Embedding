clear all;
addpath('C:\Users\ChenKx\Desktop\tensorsvd\');

Filepath=fullfile('C:\Users\ChenKx\Desktop\tensorsvd\function\');
list1=dir(Filepath);
filenamem={list1.name};
sizefile=size(filenamem);
lenn=sizefile(2);
programnumber=2; %number of program
item=60; % max embedding number
number=2500; %number of functions
M=ones(item,number,programnumber);
X=double(M);
for i=3:lenn
    FilePah=strcat('C:\Users\ChenKx\Desktop\tensorsvd\function\',filenamem(i),'\');
    
    listt=dir(strjoin(FilePah));
   
    listlen=size(listt);
    EM=zeros(item,number);
    filename={listt.name};
    for k=3:(listlen(1));
        filename(k);
        path = strjoin(strcat(FilePah,filename(k)));
        load(path); %load emdedding mat
        D=C; %embedding mat name
        %disp(D);
        [m,n]=size(D)
        if m<=item
            EM(1:m,k)=D;
        else
            EM(:,k)=D(1:item,1);
    
        end
      
    end
    
    X(:,:,i-2)=EM;
end
X(:,:,1)
kcompress=5;%compress feature
%disp(X)
[U,S,V]=tensor_t_svd(X);
MM=ones(kcompress,item,programnumber);
Ucompress=double(MM);
for kk=1:programnumber
    
    Ucompress(:,:,kk)=U(1:item,1:kcompress,kk)';
end

CC=tproduct(Ucompress,X);

save('G:/tsvd/tensor.mat', 'CC');


