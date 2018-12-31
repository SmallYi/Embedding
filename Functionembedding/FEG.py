import numpy as np
from sympy import *
def constrain1(C):
    flag=0
    flagbool=0
    for i in C:
        if int(i)>=0:
            flag=flag+1
    if flag==len(C):
        flagbool=1
    return flagbool

def constrain2(fun,C):
    flag=0
    flagbool=0
    for i in C:
        im=symbols('i')
        if diff(fun,im)>=0:
            flag=flag+1
    if flag==len(C):
        flagbool=1
    return flagbool

def constrain3(fun,C):
    flag=0
    flagbool=0
    for i in C:
        im=symbols('i')
        if int(i)*diff(fun,im)==0:
            flag=flag+1
    if flag==len(C):
        flagbool=1
    return flagbool

def processU(mmatrixU,saveU):
    documentU=[]
    for line in mmatrixU:
        linenew=line[:saveU]
        documentU.append(linenew)
    return documentU


def adjmat(Wei,C):
    (m,n)=np.shape(Wei)
    s=0
    for i in m:
        for j in n:
            if Wei[i][j]==1:
                s=s+math.pow(C[i]-C[j],2)
    return s

def FEG(Att,Sim,Wei,maxiternum,tol):
    (m,n)=np.shape(Att)
    U,S,V=np.linalg.svd(Att)
    cinital=processU(U,1)
    for t in maxiternum:
        cini=np.zeros(m)
        fun=1.0/2*np.linalg.norm(Sim-C*np.transpose(C))+1.0/2*adjmat(Wei,C)