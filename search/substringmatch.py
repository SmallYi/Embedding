import numpy as np
import os
total=14586
path='C://Users//ChenKx//Desktop//TSVD//result'
namematch=os.listdir(path)
for file in namematch:
    print file
    filetemp=open(path+'//'+file)
    filetempline=filetemp.readlines()
    target=filetempline[0]

    targetbinaryname = (str(target.strip('\n')).split(':')[1]).split('_')[0]
    targetfunctionname = (str(target.strip('\n')).split(':')[2])
    #print targetbinaryname,targetfunctionname
    #print key
    startline=1
    TPRcount = 0
    FPRcount = 0
    number=0
    #print len(filetempline)
    for linee in range(len(filetempline)):
        #print filetempline[linee]=="#####"
        #print filetempline[linee].find('null:null#')
        if linee==0:
            continue
        if filetempline[linee].find('null:null#')==0:
            break
        if (linee)==startline:
            #print filetempline[linee]

            key = int(str(filetempline[linee]).split(' ')[0].split(':')[1])
            mmm=int(str(filetempline[linee]).split(' ')[3].split(':')[1])
            startline = startline + key + 1
            if TPRcount>mmm:
                TPRcount=mmm-1;
            print key, mmm,startline
            print 'TPR: ', float(TPRcount) / float(mmm)
            print  'FPR: ', float(key - TPRcount) / (total - mmm)
            TPRcount = 0
            FPRcount = 0

            continue
        else :
            testfunctioname=filetempline[linee].split('#')
            #print startline
           # print testfunctioname
            #print TPRcount, FPRcount
            #test=filetempline[linee].split('#')
            #print len(test)
            if (len(testfunctioname)-1)==1:
                testbinaryname = (str(testfunctioname[0]).split(':')[0]).split('_')[0]
                if testbinaryname.find(targetbinaryname) != -1:
                    TPRcount=TPRcount+1
                else:
                    FPRcount=FPRcount+1
            else:
                testlist=0
                for testi in range(len(testfunctioname)-1):
                    testbinaryname=(str(testfunctioname[testi]).split(':')[0]).split('_')[0]
                   # print testbinaryname
                    if testbinaryname.find(targetbinaryname)!=-1:
                        testlist=testlist+1
                #print testlist
                if (testlist)>key:
                    testlist=key

                if testlist!=0:
                    for testi in range(testlist):
                       # testbinaryname=(str(test[testi]).split(':')[0]).split('_')[0]
                        testfunctionname = ((str(testfunctioname[testi]).split(':')[1]))
                        #print testfunctionname
                        lentar=len(targetfunctionname.split('_'))
                        issame=False
                        for i in range(lentar):
                            temp=targetfunctionname.split('_')[i]
                        #issame=False
                            if testfunctionname.find(temp)!=-1:
                                    issame=True
                                    break
                        if issame:
                            TPRcount=TPRcount+1
                        else:
                            FPRcount=FPRcount+1


            #print TPRcount,FPRcount


    #print number







