import numpy as np

def searchnew(test,model):
    #testindex=list()
    i=0
    totaly=[]
    for testi in range(len(test)):
        print test[testi]
        testindex = list()
        y=[]
        for modeli in range(len(model)):
            dis=np.linalg.norm(np.array(test[testi])-np.array(model[modeli]))
            testindex.append({'index':modeli,'dis':dis})
            i=i+1
        testindex.sort(key=lambda x:x['dis'],reverse=False)
        for x in testindex[0:3]:
            y.append(x['index'])
        totaly.append(y)
        print totaly
    return totaly

test=[[1,2,3,4],[2,3,4,1],[6,5,4,7]]
model=[[1,2,3,4],[2,3,4,5],[5,5,4,7],[7,6,4,8],[6,7,8,9],[4,5,6,7]]
searchnew(test, model)

