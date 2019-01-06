import numpy as np
import scipy.io as scio
import scipy.io
import os
#import util
number=0
#file='tensor.mat' ;
#files= os.listdir(path);
s =scio.loadmat('embeddd/tensor.mat');
#path1='opensslarmo3/embeddd/' ;
#files1= os.listdir(path1)
svec=s['CC']
n1,n2,n3=np.shape(svec)
slicee=[]
data=np.zeros((n1,n2))
for i in range(n3):
    data[:,:]=svec[:,:,i]
    slicee.append(data)

distt=[]  
# test K with recall
#ROC
testindex=0
K=0.1

numberlist=[]
Recalllist=[]
test=slicee[testindex]
for j in range(len(slicee)):
    number=0
    for jj in range(len(slicee[i])):
        dvec=slicee[j][:,jj]
        for jjj in range(len(test)):
            tdev=test[:,jjj]
            dist=np.linalg.norm(sum(dvec)-sum(tdev));
        #print(dist);
            distt.append(dist[0]);
        ds=sorted(list(distt));
        if ds[0]<=K:
            number=number+1;
            positive=number/max(jj,jjj)
    Recalllist.append(positive)

#because a slcie in tensor represent a program, map(Recalllist.index, positive).
# if positive is high, and its index belongs 
#to different optimation level programs or different aritchture programs, positive is TPR
#if positive is low, and its index belongs to other programs. positive is FPR. you can set
#the different test, you can choose two or more programs. you best to test one program at one time.

#     if not os.path.isdir(file1):
#         s =scio.loadmat(path1+file1);

#         svec=s['C'];
# #print(svec);
#         distt=[]
#         for file in files:
#             if not os.path.isdir(file):
#                 f=scio.loadmat(path+file);
#                 fvec=f['C'];
#        # print(sum(fvec));
#                 dist=abs(sum(fvec)-sum(svec));
#         #print(dist);
#                 distt.append(dist[0]);
#         ds=sorted(list(distt));
#         if ds[0]<=0.1:
#             number=number+1;
# Recall=number/max(np.shape(svec))






    