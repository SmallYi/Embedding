#coding=utf-8
import re
import math
import itertools
import numpy as np
import tensorflow as tf
#import pandas as pd
import datetime
import threading
import numpy
import scipy
import unittest
import os
import nearpy.utils.utils
#import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist, squareform
from scipy.spatial.distance import pdist
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs
#from nearpy import Engine
#from nearpy.distances import CosineDistance
#from nearpy.hashes import RandomBinaryProjections, RandomBinaryProjectionTree, HashPermutations, HashPermutationMapper

def processU(matric_U,Save_N_Singular_value):
    """according to the matric U, choose the words as the feature in each document,根据前N个奇异值对U进行切分,选择前N列""" 
    document_matric_U=[]
    for line in matric_U:
        line_new=line[:Save_N_Singular_value]
        document_matric_U.append(line_new)
    return document_matric_U

def processS(matric_S,Save_information_value):
    """choose the items with large singular value,根据保留信息需求选择奇异值个数"""
    matricS_new=[]
    S_self=0
    N_count=0
    Threshold=sum(matric_S)*float(Save_information_value)
    for value in matric_S:
        if S_self<=Threshold:
            matricS_new.append(value)
            S_self+=value
            N_count+=1
        else:
            break
    print ("the %d largest singular values keep the %s information " %(N_count,Save_information_value))
    return (N_count,matricS_new)


def processSS(matric_S,Save_N_Singular_value):
    """根据前N个奇异值对V进行切分,选择前N行"""
    #document_matric_S=[]
    document_matric_SS=matric_S[:Save_N_Singular_value]
    return document_matric_SS

def processV(matric_V,Save_N_Singular_value):
    """根据前N个奇异值对V进行切分,选择前N行"""
    document_matric_V=matric_V[:Save_N_Singular_value]
    return document_matric_V
def pad(M):
    MM=np.zeros((200,1))
    
    if len(M)>=200:
        MM=M[:200]
    else:
        MM[:len(M)]=M
            
def tensor_t_compress(A,k,n,m):
    D = tf.fft3d(A);
   
    #n = np.shape(A,3);
    Uy=tf.Variable(tf.zeros(k,m,n))
    for i in n:
        Ux,Sx,Vx = np.linalg.svd(D[:,:,i])
        Uy[:,:,i].assign(processU(Ux,k))
       # Sy[:,:,i] = processS(Sx,k)
       # Vy[:,:,i] = processV(Vx,k)
 
  
 #   U = ifft(Uy,[],3);
 #   S = ifft(Sy,[],3);
 #   V = ifft(Vy,[],3);
    (n1,n2,n3) =tf.shape(Ux)
    (m1,m2,m3) = tf.shape(A)

   # if n2!= m1 and n3 != m3： 
  #      error('Inner tensor dimensions must agree.');

    C =tf.Variable(tf.zeros(n1,m2,n3));

# first frontal slice
    

    halfn3 = np.round(n3/2.0)
    for i in range(halfn3):
        C[:,:,i].assign(np.transpose(Ux[:,:,i])*D[:,:,i])
        C[:,:,n3+2-i].assign(np.conjuate(C[:,:,i]))
    C[:,:,1].assign(np.dot(np.transpose(Ux[:,:,1]),A[:,:,1]))

    if np.mod(n3,2) == 0:
        i = halfn3+1
        C[:,:,i].assign(np.transpose(Uy[:,:,i])*D[:,:,i])

    C = tf.spectral.ifft3d(C)
    return C


import scipy.io  as sio

s=[]
k=25
Tmat=tf.Variable(tf.zeros((200,5000,1)))
pathh='functions/'
files=os.listdir(pathh)
for functionfile in files:
    j=0
    if os.path.isdir(functionfile): 
        path1=functionfile+'/'
        files=os.listdir(path1)
        FMat=np.zeros((200,5000))
        i=0
        for file in files:
            if not os.path.isdir(file):
                Embed=sio.loadmat(path1+file)
                E=Embed["H_AANE"]
                #print(E)
                Epad=pad(E)
                FMat[:,i]=Epad
                i=i+1
        Tmat[:,:,j].assign(FMat[:,i])
        print(Tmat[:,:,j])
        j=j+1

C=tensor_t_compress(Tmat,k,1,200)
       
        
