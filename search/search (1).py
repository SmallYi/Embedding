import numpy as np
import scipy.io as scio
import scipy.io
import os
import math
#import util
#number=0
#file='tensor.mat' ;
#path='opensslx86/embeddd1/'
#path='busyboxarm/embeddd1/'
#files= os.listdir(path)
#path1='busybox86/embeddd1/'
#files1= os.listdir(path1)
#for file in files:

 #   if not os.path.isdir(file):
 #       s =scio.loadmat(path+file)
  ##      svec=s['C']
# #print(svec);
 #       distt=[]
 #       for file1 in files1:
 #            if not os.path.isdir(file1):
  #               f=scio.loadmat(path1+file1);
    #             fvec=f['C'];
                # print(fvec);
    #             dist=abs(sum(fvec[0])-sum(svec[0]));
                # print(dist);
  #              if dist=='nan':
          #           dist=0
     #            distt.append(dist)
      #  ds=sorted(list(distt));
      #  print ds[0]
      #  if ds[0]<=0.01:
     #       number=number+1;

#print number
# Recall=number/max(np.shape(svec))

import numpy as np
import scipy.io as scio
import scipy.io
import os
#import util
number=0
#file='tensor.mat' ;
#files= os.listdir(path);
s =scio.loadmat('tensor.mat');
#path1='opensslarmo3/embeddd/' ;
#files1= os.listdir(path1)
svec=s['FFE']
n1,n2,n3=np.shape(svec)
slicee=[]
data=np.zeros((n1,n3))
for i in range(n2):
    data[:,:]=svec[:,i,:]
    slicee.append(data)
    #print data

    data = np.zeros((n1, n3))

distt=[]
#print slicee
# test K with recall
#ROC
testindex=0
K=0.01

numberlist=[]
Recalllist=[]
test=slicee[0]
#(mmm,nnn)=np.size(test)
#print slicee[0]

#dist=np.linalg.norm(slicee[0]-slicee[2])
#print dist
for j in range(len(slicee)-1):
    number=0;
 #   for i in range(len(slicee)):
 #       dist=sum(sum(slicee[j]))-sum(sum(slicee[i]));
  #      print dist
  #  print '\n'


    for jj in range(len(slicee[j+1][0])):
        dvec=slicee[j+1][:,jj]
        distt = []
       # print dvec
        for jjj in range(len(test[0])):
            tdev=slicee[testindex][:,jjj]
            #print tdev-dev
            if np.linalg.norm(dvec)!=0 and np.linalg.norm(tdev)!=0:
                dist=np.linalg.norm(dvec-tdev)
        #print(dist);
    #print dist
                distt.append(abs(dist))
    #print distt
        ds=sorted(list(distt))
        #print ds
        #print '\n'
        if ds:
            if ds[0]<=K:
                number=number+1
    print number
     #   positive=number/max(jj,jj)
#Recalllist.append(positive)

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






    