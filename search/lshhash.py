from lshash import LSHash
import scipy.io
import numpy as np
import random
import os
import time
import array
np.set_printoptions(suppress=True,precision=6,threshold=8)
pathtensor='tensor.mat'
s =scipy.io.loadmat(pathtensor)
svec=s['FFE']
#print svec[:,1,0]
datalen=len(svec)
n1,n2,n3=np.shape(svec)
#print n1,n2,n3
binarytxt=open('binaryname.txt','w')
functiontxt=open('functionname.txt','w')
data=np.zeros((n1,87212))
m=0
binarynameindex=[]
functionnameindex=[]
for i in range(n2):
    for j in range(n3):
        if svec[:,i,j].all()!=0:
            binarynameindex.append(i)
            functionnameindex.append(j)
            data[:,m]=svec[:,i,j]
            m=m+1
#print data[:,0]

dataves=np.transpose(data)
#print len(dataves)
modelindex=list(set(np.random.randint(1,87212,size=10000)))
for iii in range(len(modelindex)):
    #print binarynameindex[iii],functionnameindex[iii]
    binarytxt.write(str(binarynameindex[iii])+'\n')
    functiontxt.write(str(functionnameindex[iii])+'\n')
lsh_model=LSHash(7,n1)
for jj in modelindex:
    lsh_model.index(dataves[jj,:])

#data=np.transpose(data)
#num_random=15
#lsh_model.train(num_random)

# if you want to test a program
starttest=1 #start test index
endtest=5
testindex=random.sample(modelindex,1) #SIZE IS THE NUMBER OF TEST FUNCTIONS

#if you want to test a single function.
#testindex=set(np.random.randint(n3*n2,size=1))

#print testindex[5]

test=np.zeros((len(testindex),n1))
for i in range(len(testindex)):
  #  print dataves[testindex[i],:]
    test[i,:]=dataves[testindex[i],:]
#print len(test)
output=open('result.txt','w')
timee=open('time.txt','w')
for queryi in range(len(testindex)):
    print binarynameindex[modelindex.index(testindex[queryi])],functionnameindex[modelindex.index(testindex[queryi])]
    if test[queryi,:].all()!=0:
        starttime=time.time()
        Atemp=lsh_model.query(test[queryi,:],5,'cosine')
        print (str(Atemp[0]).split(')')[0]).replace('(','')
        output.write((str(Atemp[0]).split(')')[0]).replace('(','')+'\n')
        output.write((str(Atemp[1]).split(')')[0]).replace('(', '') + '\n')
        output.write((str(Atemp[2]).split(')')[0]).replace('(', '') + '\n')
        output.write((str(Atemp[3]).split(')')[0]).replace('(', '') + '\n')
        output.write((str(Atemp[4]).split(')')[0]).replace('(', '') + '\n')

        endtime=time.time()
        timee.write(str(endtime-starttime)+'\n')
       # output.write(A)
        output.write('\n')

output.close()
binarytxt.close()
functiontxt.close()
timee.close()