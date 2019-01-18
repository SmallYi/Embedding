clear all;
addpath('E:\tsvd\');

Filepath=fullfile('E:\tsvd\embeddd');
list1=dir(Filepath);
filenamem={list1.name};
sizefile=size(filenamem);
lenn=sizefile(2);
programnumber=18; %number of program
item=80; % max embedding number
number=3220; %max number of functions in a program
M=ones(item,programnumber,number);
X=double(M);
for i=3:lenn
    filenamem(i)
    FilePah=strcat('E:\tsvd\embeddd\',filenamem(i),'\');
    
    listt=dir(strjoin(FilePah));
   
    listlen=size(listt);
    EM=zeros(item,number);
    filename={listt.name};
    for k=3:(listlen(1));
        filename(k);
        path = strjoin(strcat(FilePah,filename(k)));
        load(path); %load emdedding mat
        D=FE; %embedding mat name
        %disp(D);
        [m,n]=size(D);
        if m<=item
            EM(1:m,k)=(D);
        else
            EM(:,k)=(D(1:item,1));
    
        end
      
    end
    
    X(:,i-2,:)=EM;
end
X(:,:,1);
kcompress=15;%compress feature
%disp(X)
% M=ones(6,8,5);
% X=double(M);
% X1=ones(6,1,5)
% X(:,1,:)=[11 22 33 44 51;21 23 54 65 67;43 34 35 26 27;62 71 43 42 225;22 883 36 65 47;76 84 51 76 97];
% X(:,2,:)=[62 71 43 42 225;22 883 36 65 47;76 84 51 76 97;23 51 52 52 35;32 34 35 35 373;635 65 47 86 67];
% X(:,3,:)=[23 51 52 52 35;32 34 35 35 373;635 65 47 86 67;23 51 52 52 35;32 34 35 35 373;635 65 47 86 67];
% X(:,4,:)=[33 64 56 62 16;26 636 26 651 63; 64 57 56 34 12;11 22 33 44 51;21 23 54 65 67;43 34 35 26 27];
% X(:,5,:)=[2 1 3 2 5;2 3 3 5 7;6 4 1 6 7;11 22 33 44 51;21 23 54 65 67;43 34 35 26 27];
% X(:,6,:)=[2 1 2 2 5;2 4 5 5 7;6 6 4 6 7;33 64 56 62 16;26 636 26 651 63; 64 57 56 34 12];
% X(:,7,:)=[3 4 5 2 1;2 3 2 1 3;4 5 6 4 2;33 64 56 62 16;26 636 26 651 63; 64 57 56 34 12];
% X(:,8,:)=[21 22 44 45 65;42 43 44 45 46;43 44 51 16 17;21 22 44 45 65;42 43 44 45 46;43 44 51 16 17]
% 
% M1=ones(6,7,5);
% Y=double(M);
% Y(:,1,:)=[11 22 33 44 51;21 23 54 65 67;43 34 35 26 27;62 71 43 42 225;22 883 36 65 47;76 84 51 76 97]
% Y(:,2,:)=[62 71 43 42 225;22 883 36 65 47;76 84 51 76 97;23 51 52 52 35;32 34 35 35 373;635 65 47 86 67]
% Y(:,3,:)=[23 51 52 52 35;32 34 35 35 373;635 65 47 86 67;23 51 52 52 35;32 34 35 35 373;635 65 47 86 67]
% Y(:,4,:)=[33 64 56 62 16;26 636 26 651 63; 64 57 56 34 12;11 22 33 44 51;21 23 54 65 67;43 34 35 26 27]
% Y(:,5,:)=[2 1 3 2 5;2 3 3 5 7;6 4 1 6 7;11 22 33 44 51;21 23 54 65 67;43 34 35 26 27]
% Y(:,6,:)=[2 1 2 2 5;2 4 5 5 7;6 6 4 6 7;33 64 56 62 16;26 636 26 651 63; 64 57 56 34 12]
% Y(:,7,:)=[3 4 5 2 1;2 3 2 1 3; 4 5 6 4 2;33 64 56 62 16;26 636 26 651 63; 64 57 56 34 12]
% X1=X(:,8,:)
% %X2=[2 1 3 2 5;2 3 3 5 7;6 4 1 6 7]
[U,S,V]=tensor_t_svd(X);
% [U1,S1,V1]=tensor_t_svd(Y);
% % [U2,S2,V2]=tensor_t_svd(X2);
% C1=U1(:,1:2)'*X1
% C2=U2(:,1:2)'*X2
MM=ones(item,kcompress,number);
Ucompress=double(MM);
%Vcompress=double(MM);
for kk=1:number
    
    Utemp=U(:,1:kcompress,kk);
   % Vcompress(:,:,kk)=U1(:,1:kcompress,kk);
    Ucompress(:,:,kk)=Utemp;
end
% 
FFE=double(ones(kcompress, programnumber,number));

Up=permute(Ucompress,[2,1,3]);
% Umat=double(ones(number*kcompress,number*item));
% Xmat=double(zeros(item*number,programnumber));
% for kkkk=1:number
%     Umat((kkkk-1)*kcompress+1:(kkkk)*kcompress,(kkkk-1)*item+1:(kkkk)*item)=Up(:,:,kkkk);
%     Xmat((kkkk-1)*item+1:(kkkk)*item,:)=X(:,:,kkkk);
% end
for kkk=1:number
    FFE(:,:,kkk)=abs(Up(:,:,kkk)*X(:,:,kkk));
end
% FFEmat=Umat*Xmat;
% for kkk=1:number
%     FFE(:,:,kkk)=FFEmat((kkkk-1)*kcompress+1:(kkkk)*kcompress,:);
% end
%CC=tproduct(permute(Ucompress,[2,1,3]),X);
%CCC=tproduct(permute(Vcompress,[2,1,3]),X1);
%diffvec=sqrt(sum((CC(:,1,1)-CC(:,2,1)).^2));
save('G:/tsvd/tensor.mat', 'FFE');


