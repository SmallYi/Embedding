
import numpy
import scipy.io
import os
#import util
path='opensslarmo3/node/' 
files= os.listdir(path)
s = []
for file in files:
    if not os.path.isdir(file):
        f = open(path+file)
        tt=f.readlines()
        fline=len(tt)
        
        
        
        
        
        
        
        
        
        
        
        print(fline)
        a=int(fline)
        network=numpy.zeros((a-1,6))
        j=tt[0].split(':')[0]
        if a>2:
            #print(file)
            for line in tt[1:fline]:
                i=0
                edge=[]
                tempconnectnode = line.strip('\n').strip('}').strip(']').split(',')
                #print(tempconnectnode)
                tempconnectnode_len=len(tempconnectnode)
                aaa=tempconnectnode[int(tempconnectnode_len)-6:int(tempconnectnode_len)]
                if tempconnectnode_len>1:
                    for tempite in range(6):
                     #   print(tempconnectnode[int(tempite)+1])
                        #if aaa[int(tempite)+1] !=' []':
                        network[i][int(tempite)]=int(aaa[int(tempite)])
                            
                i=i+1
        #j=j+1
            scipy.io.savemat('opensslarmo3/att/'+str(j)+'.mat', mdict={'network': network})





         




