import numpy as np
import math
import os
import scipy.io as sio
import time

def processU(U,k):
    proU=[]
    for line in U:
        linenew=line[:k]
        proU.append(linenew)
    return proU

def diaa(C,Sim,Wei,kk,tol):
    (nn,nn)=np.shape(Wei)
    #print(n)
    a=0.0
    for jj in range(nn):
       # print(C[jj][0]*C[kk][0]-Sim[jj][kk])
        #print(C[kk][0]) 
        a=a+2.0*(C[jj]*C[kk]-Sim[jj][kk])*C[jj]+1.0/2*(Wei[kk][jj]+Wei[jj][kk])
        if a<tol:
            a=0
    #print a
    return a

def FEG(Att,Sim,Wei,tol,maxitem):
    U,S,V=np.linalg.svd(Att)
    (m,n)=np.shape(Wei)
    C=np.zeros(m)
    Cinital=processU(U,1)
    #C=Cinital[:m]
    #print C
    #print(m)
    #print(C)
    Ch=np.zeros(m)
    for t in range(maxitem):
        for i in range(m):
            #print(C[i][0])
            b=Sim[i][i]-math.pow(C[i],2)
           # print(b)
            if math.pow(np.linalg.norm(C),2)!=0:
                d=math.fabs(float(diaa(C,Sim,Wei,i,tol)/2.0)/math.pow(np.linalg.norm(C),2))
            else:
                d=0
            #print d
            #print math.pow(np.linalg.norm(C),2)
            D=-b+math.pow(C[i],2)+2.0*C[i]*d+float(math.pow(d,2)/2.0)
            ch=C[i]-(1.0/(2*(np.linalg.norm(C)+D)))*(diaa(C,Sim,Wei,i,tol))
           # print ch
            if math.pow(np.linalg.norm(C),2)+math.pow(D,2)==0:
                C[i]=np.sqrt(b)
            else:

                C[i] = ch


            #print C[i]wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
            #if C[i]>=0 and diaa(C,Sim,Wei,i)>=0 and C[i]*diaa(C,Sim,Wei,i)==0:
    print C          #  break
            ################################################################################################print(C)
    return C

path='network/'
files=os.listdir(path)
s=[]
for file in files:
    if not os.path.isdir(file):
        print(file)

        tol=10**-0.6
        maxitem=200
        GG=sio.loadmat(path+file)
        G=GG["network"]
        G_name=os.path.basename(path+file)
        A_name='node'+G_name[4:]
        AA=sio.loadmat('att/'+A_name)
        A=AA['network']
        #print G
        (mm,mm)=np.shape(G)
        (mmm,nn)=np.shape(A)
        #C = np.zeros(mm)
        S=np.zeros((mm,mm))
        Q=np.zeros((mm,nn))
        #for ii in range(mm):
        #    print(A[ii,:])
        #    for jj in range(mm):
        #       # print(A[ii,:])A[jj])
        #        if (np.linalg.norm(A[ii,:])!=0) and np.linalg.norm(A[jj,:])!=0:                                                             
        #            S[ii][jj]= float(np.dot(A[ii,:],np.transpose(A[jj,:])))/(np.linalg.norm(A[ii,:])*np.linalg.norm(A[jj,:]))
        #        else:
        #           S[ii][jj]=0
       ######################################### print(A) 
        #print(S)
        #for jj in range(mm):
        #    Q[jj]=np.sqrt(A[jj]*A[jj])
        #for ii in range(mm):
        #   Stemp=np.dot(A[ii,:],np.transpose(A))
          # print(np.dot(np.sqrt(A[ii]*A[ii]),np.transpose(Q)))
         #  S[ii]=float(Stemp[:mm])*(1.0/np.dot(np.sqrt(A[ii]*A[ii]),np.transpose(Q)))
        #print(A)
        C=np.zeros(mm)
        for jj in range(mm):
            #print A[jj]
            for ii in range(mm):
                #print A[ii]
                S[jj][ii]=float(np.dot(A[ii],A[jj]))/(np.linalg.norm(A[ii])*(np.linalg.norm(A[jj])))

        tol=0.0001
        C=FEG(A,S,G,tol,maxitem)
        starttime=time.time()
        #print(C)
        embedding_name='embedding'+G_name[4:]
        sio.savemat('embeddd/'+embedding_name, {"C":C})
        


        
