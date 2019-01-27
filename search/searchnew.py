from lshash import LSHash
import scipy.io
import numpy as np
pathtensor='tensor.mat'
s =scipy.io.loadmat(pathtensor)
svec=s['FFE']
#print svec[:,1,0]
datalen=len(svec)
n1,n2,n3=np.shape(svec)
#print n1,n2,n3
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

testindex=list(set(np.random.randint(1,87212,size=1000)))

test=np.zeros((len(testindex),n1))
for i in range(len(testindex)):
  #  print dataves[testindex[i],:]
    test[i,:]=dataves[testindex[i],:]
#print len(test)
listA=[]
for queryi in range(len(testindex)):
    print test[queryi,:]
    listAA=[]
    max=9999
    for jj in range(87212):
        A=np.linalg.norm(test[queryi,:]-dataves[jj,:])
        if A<max:
            max=A
        listA.append(A)
    listA.append(listAA)

for i in range(len(listA)):
    temp=sorted(listA[i])
    print temp[0:5]

