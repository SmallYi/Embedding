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

def diaa(C,Sim,Wei,kk):
    (nn,nn)=np.shape(Wei)
    #print(n)
    a=0.0
    for jj in range(nn):
       # print(C[jj][0]*C[kk][0]-Sim[jj][kk])
        #print(C[kk][0]) 
        a=a+2.0*(C[jj][0]*C[kk][0]-Sim[jj][kk])*C[jj][0]+1.0/2*(Wei[kk][jj]+Wei[jj][kk])
    #print(a)
    return a

def FEG(Att,Sim,Wei,tol,maxitem):
    U,S,V=np.linalg.svd(Att)
    (m,n)=np.shape(Wei)
    Cinital=processU(U,1)
    C=Cinital[:m]
    #print(m)
    #print(C)
    Ch=np.zeros(m)
    for t in range(maxitem):
        for i in range(m):
            #print(i)
            b=Sim[i][i]-math.pow(C[i][0],2)
            #print(b)
            if math.pow(np.linalg.norm(C),2)!=0:
                d=float(diaa(C,Sim,Wei,i))/math.pow(np.linalg.norm(C),2)
            else:
                d=0
                    
            D=max(0,0-b+math.pow(C[i],2)+2.0*C[i][0]*d+float(math.pow(d,2)/2.0))
            ch=C[i][0]-(1.0/2*np.linalg.norm(C)+D)*(diaa(C,Sim,Wei,i))
            if math.pow(np.linalg.norm(C),2)+math.pow(D,2)==0:
                C[i][0]=np.sqrt(b)
            else:
                C[i][0]=max(0,ch)
            #if C[i]>=0 and diaa(C,Sim,Wei,i)>=0 and C[i]*diaa(C,Sim,Wei,i)==0:
              #  break
            ################################################################################################print(C)
    return C

path='opensslarm/network/'
files=os.listdir(path)
s=[]
for file in files:
    if not os.path.isdir(file):
        print(file)
        tol=10**-0.6
        maxitem=400
        GG=sio.loadmat(path+file)
        G=GG["network"]
        G_name=os.path.basename(path+file)
        A_name='graph_'+G_name[6:]
        AA=sio.loadmat('opensslarm/att/'+A_name)
        A=AA['network']
        (mm,mm)=np.shape(G)
        (mmm,nn)=np.shape(A)
        S=np.zeros((mm,mm))
        Q=np.zeros((mm,nn))
        #for ii in range(mm):
        #    print(A[ii,:])
        #    for jj in range(mm):
        #       # print(A[ii,:])
        #        if (np.linalg.norm(A[ii,:])!=0) and np.linalg.norm(A[jj,:])!=0:                                                             
        #            S[ii][jj]= float(np.dot(A[ii,:],np.transpose(A[jj,:])))/(np.linalg.norm(A[ii,:])*np.linalg.norm(A[jj,:]))
        #        else:
        #           S[ii][jj]=0
       ######################################### print(A) 
        #print(S)
        for jj in range(mm):
            Q[jj]=np.sqrt(A[jj]*A[jj])
        for ii in range(mm):
            Stemp=np.dot(A[ii,:],np.transpose(A))
            print(np.dot(np.sqrt(A[ii]*A[ii]),np.transpose(Q)))
            S[ii]=float(Stemp[:mm])*(1.0/np.dot(np.sqrt(A[ii]*A[ii]),np.transpose(Q)))
        #print(A)
        #for jj in range(mm):
        #    for ii in range(mm):
        #        S[jj][ii]=float(np.linalg.norm(A[ii]-A[jj]))
       # print(S)
        starttime=time.time()
        C=FEG(A,S,G,tol,maxitem)                                               
        starttime=time.time()
        #print(C)
        embedding_name='embedding'+G_name[6:]
        sio.savemat('opensslarm/embeddd/'+embedding_name, {"C":C})
        


        
