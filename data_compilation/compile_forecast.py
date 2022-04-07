import csv
import re
import pickle as pkl
import os
import pandas as pd


def my_sum(*args):
    return sum(args)
def reverse(sequence):
    sequence = list(sequence)
    for i in range(len(sequence)):
        if sequence[i] == 'A':
            sequence[i] = 'T'
        elif sequence[i] == 'T':
            sequence[i] = 'A'
        elif sequence[i] == 'G':
            sequence[i] = 'C'
        else:
            sequence[i] = 'G'
    sequence = ''.join(sequence)
    return sequence
def rawdata(path1,path2):
    dataA = []
    for line in open(path1 ,"r"):  # 设置文件对象并读取每一行文件
        line=line[:-1]
        line=line.split('	')
        dataA.append(line)
    dataB = []
    for line in open(path2 ,"r"):  # 设置文件对象并读取每一行文件
        line=line[:-1]
        line=line.split('	')
        dataB.append(line)

    num1=[]
    for i in range(len(dataA)):
        if len(str(dataA[i]))<=20:
            p=i
            num1.append(p)
        elif i==len(dataA)-1:
            num1.append(len(dataA))
        else:
            p=p
    num2=[]
    for i in range(len(dataB)):
        if len(str(dataB[i]))<=20:
            p=i
            num2.append(p)
        elif i==len(dataB)-1:
            num2.append(len(dataB))
        else:
            p=p

    datalistall1 = []
    for i in range(len(num1) - 1):
        datalist = []
        for j in range(num1[i], num1[i + 1]):
            datalist = datalist + dataA[j]
        if len(datalist)!=1:
            datalistall1.append(datalist)
        else:
            continue

    datalistall2 = []
    for i in range(len(num2) - 1):
        datalist = []
        for j in range(num2[i], num2[i + 1]):
            datalist = datalist + dataB[j]
        if len(datalist)!=1:
            datalistall2.append(datalist)
        else:
            continue

    for i in range(len(datalistall1)):
        n=0
        for j in range(len(datalistall2)):
            if datalistall1[i][0]!=datalistall2[j][0]:
                n=n+1
        if n==len(datalistall2):
            print(datalistall1[i])
    print(len(datalistall2))

    datalistall3 = []
    for i in range(len(datalistall1)):
        n=0
        for j in range(len(datalistall2)):
            if datalistall1[i][0] == datalistall2[j][0]:
                n=j
        datalistall3.append(datalistall2[n])
    datalistall2=datalistall3
    # print(datalistall3[3170])
    # print(datalistall1[3170])
    # a=[]
    # b=[]
    # n=0
    # for i in range(len(datalistall1)):
    #     a1=0
    #     for j in range(2,len(datalistall1[i]),3):
    #         a1=my_sum(a1,int(datalistall1[i][j]))
    #     a2=0
    #     for k in range(2,len(datalistall2[i]),3):
    #         a2=my_sum(a2,int(datalistall2[i][k]))
    #     if my_sum(a1,a2)>100:
    #         a.append(datalistall1[i])
    #         b.append(datalistall2[i])
    #         n=n+1
    a=datalistall1
    b=datalistall2
    # print(n)
    # print(a[0:10])
    # print(b[0:10])
    # print(len(a))
    # print(len(b))
    # print(a[3170][0])
    # print(b[3170])
    # for i in range(len(a)):
    #     if a[i][0]!=b[i][0]:
    #         print(i)
    #         print(a[i][0])
    #         print(b[i][0])
    for i in range(len(a)):
        if a[i][0]=='@@@Oligo71640' or a[i][0]=='@@@Oligo71769' or a[i][0]=='@@@Oligo80844':
            continue
        else:
            for j in range(1, len(a[i]), 3):
                for k in range(1, len(b[i]), 3):
                    if a[i][j] == b[i][k]:
                        a[i][j + 1] = my_sum(int(a[i][j + 1]), int(b[i][k + 1]))
            for l in range(1, len(b[i]), 3):
                n = 0
                for m in range(1, len(a[i]), 3):
                    if b[i][l] != a[i][m]:
                        n = n + 1
                if n == (len(a[i]) - 1) / 3:
                    a[i].append(b[i][l])
                    a[i].append(b[i][l + 1])
                    a[i].append(b[i][l + 2])
    return a
def supplementarydata(path):
    forecastdata=[]
    with open(path) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for ll in reader:
            forecastdata.append(ll)

    forecastdata1=[]
    for i in range(1,len(forecastdata)):
        if forecastdata[i][3] == 'Improved' :
            if forecastdata[i][7] == 'REVERSE':
                list=[]
                list.append(forecastdata[i][0])
                forecastdata[i][2] = forecastdata[i][2][::-1]
                forecastdata[i][2] = reverse(forecastdata[i][2])
                list.append(forecastdata[i][2])
                if forecastdata[i][6] != '49':
                    print(forecastdata[i][0])
                else:
                    forecastdata[i][6] = 30
                    list.append(forecastdata[i][6])
                    list.append(forecastdata[i][7])
                    forecastdata1.append(list)
            else:
                list = []
                list.append(forecastdata[i][0])
                list.append(forecastdata[i][2])
                list.append(forecastdata[i][6])
                list.append(forecastdata[i][7])
                forecastdata1.append(list)
    forecastdata=forecastdata1
    return forecastdata
def merge(forecastdata,rawdatalist):
    data=[]
    for i in range(len(forecastdata)):
        list=[]
        n=0
        for j in range(len(rawdatalist)):
            if forecastdata[i][0]!=rawdatalist[j][0]:
                n=n+1
            elif forecastdata[i][0]==rawdatalist[j][0]:
                list.append(forecastdata[i][1][int(forecastdata[i][2])-20:int(forecastdata[i][2])])
                list=list+forecastdata[i][1:]
                list=list+rawdatalist[j][1:]
        data.append(list)
        if n==len(rawdatalist):
            print(forecastdata[i][0])
    while [] in data:
        data.remove([])
    return data
def transforlabel(mergelist):
    for i in range(len(mergelist)):
        if mergelist[i][3] != 'REVERSE':
            for j in range(4,len(mergelist[i]),3):
                a = re.findall(r"-?\d+\.?\d*", mergelist[i][j])
                if len(a)<4:
                    if str(mergelist[i][j])=='I%s_L%sR%s'%(str(a[0]),str(a[1]),str(a[2])):
                        if int(a[0])>2 and int(a[0])<=20:
                            mergelist[i][j]='3'
                        elif int(a[0])>20:
                            mergelist[i][j]='break'
                        elif int(a[0])<=2:
                            x=my_sum(int(a[1]),int(mergelist[i][2])-3,1)
                            mergelist[i][j]='%s+%s'%(int(a[0]),mergelist[i][j+2][x:x+int(a[0])])
                    if str(mergelist[i][j])=='D%s_L%sR%s'%(str(a[0]),str(a[1]),str(a[2])):
                        x = my_sum(int(a[1]), 1)
                        mergelist[i][j] = '%s+%s' % (x, int(a[0]))
                    else:
                        pass
                elif len(a)==4:
                    if str(mergelist[i][j])=='I%s_L%sD%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        mergelist[i][j]='break'
                    elif str(mergelist[i][j])=='I%s_L%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        if int(a[0]) > 2 and int(a[0]) <= 20:
                            mergelist[i][j] = '3'
                        elif int(a[0]) > 20:
                            mergelist[i][j] = 'break'
                        elif int(a[0]) <= 2:
                            x = my_sum(int(a[1]), int(mergelist[i][2])-3, 1,int(a[2]))
                            mergelist[i][j] = '%s+%s' % (int(a[0]), mergelist[i][j + 2][x:x + int(a[0])])
                    elif str(mergelist[i][j])=='D%s_L%sI%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        mergelist[i][j]='break'
                    elif str(mergelist[i][j])=='D%s_L%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        x = my_sum(int(a[1]), 1,int(a[2]))
                        mergelist[i][j] = '%s+%s' % (x, int(a[0]))
                    else:
                        pass
                elif len(a)==5:
                    if str(mergelist[i][j])=='D%s_L%sI%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3]),str(a[4])) or  str(mergelist[i][j])=='I%s_L%sD%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3]),str(a[4])):
                        mergelist[i][j] = 'break'
                    else:
                        pass
                else:
                    pass
        else:
            for j in range(4,len(mergelist[i]),3):
                a = re.findall(r"-?\d+\.?\d*", mergelist[i][j])
                if len(a)<4:
                    if str(mergelist[i][j])=='I%s_L%sR%s'%(str(a[0]),str(a[1]),str(a[2])):
                        if int(a[0])>2 and int(a[0])<=20:
                            mergelist[i][j]='3'
                        elif int(a[0])>20:
                            mergelist[i][j]='break'
                        elif int(a[0])<=2:
                            # print(mergelist[i][j])
                            # print(mergelist[i][j+2])
                            x=my_sum(int(a[1]),1)
                            x=52-x
                            y=mergelist[i][j+2][x:x+int(a[0])]
                            y=reverse(y)
                            y=y[::-1]
                            mergelist[i][j]='%s+%s'%(int(a[0]),y)
                            # print(mergelist[i][j])
                    if str(mergelist[i][j])=='D%s_L%sR%s'%(str(a[0]),str(a[1]),str(a[2])):
                        x = my_sum(int(a[1]), 1)
                        mergelist[i][j] = '%s+%s' % (x, int(a[0]))
                    else:
                        pass
                elif len(a)==4:
                    if str(mergelist[i][j])=='I%s_L%sD%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        mergelist[i][j]='break'
                    elif str(mergelist[i][j])=='I%s_L%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        if int(a[0]) > 2 and int(a[0]) <= 20:
                            mergelist[i][j] = '3'
                        elif int(a[0]) > 20:
                            mergelist[i][j] = 'break'
                        elif int(a[0]) <= 2:
                            x = my_sum(int(a[1]), 1, int(a[2]))
                            x = 52 - x
                            y = mergelist[i][j + 2][x:x + int(a[0])]
                            y = reverse(y)
                            y=y[::-1]
                            mergelist[i][j] = '%s+%s' % (int(a[0]),y)
                    elif str(mergelist[i][j])=='D%s_L%sI%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        mergelist[i][j]='break'
                    elif str(mergelist[i][j])=='D%s_L%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3])):
                        x = my_sum(int(a[1]), 1,int(a[2]))
                        mergelist[i][j] = '%s+%s' % (x, int(a[0]))
                    else:
                        pass
                elif len(a)==5:
                    if str(mergelist[i][j])=='D%s_L%sI%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3]),str(a[4])) or  str(mergelist[i][j])=='I%s_L%sD%sC%sR%s'%(str(a[0]),str(a[1]),str(a[2]),str(a[3]),str(a[4])):
                        mergelist[i][j] = 'break'
                    else:
                        pass
                else:
                    pass
    return mergelist
    # mergelist= pd.DataFrame(mergelist)
    # mergelist.to_csv('mergelist.csv',index=None,header=None)
def comparisondata(mergelist):
    forecasttestdata='forecasttestdata.txt'
    fout = open(forecasttestdata, 'w')
    for i in range(len(mergelist)):
        fout.writelines(" ".join('%s' % item for item in mergelist[i][1:3]) + '\n')
    fout.close()
    for i in range(len(mergelist)):
        mergelist[i]=mergelist[i][0:3]+mergelist[i][4:]


    prerequesites =  pkl.load(open(os.path.join('model_prereq.pkl'),'rb'))
    label, rev_index, features, frame_shift = prerequesites
    value_list = list(rev_index.values())
    lindeltestdata=[]
    title2=['ID']+value_list
    lindeltestdata.append(title2)
    for i in range(len(mergelist)):
        n=int(mergelist[i][2])
        lindeltestdatalist=[]
        if n==30:
            sequence="ATG"+mergelist[i][1][0:57]
            lindeltestdatalist.append(sequence)
        else:
            sequence=mergelist[i][1][n-33:n+27]
            if len(sequence)==60:
                lindeltestdatalist.append(sequence)
            else:
                sequence=sequence+"ATGC"
                lindeltestdatalist.append(sequence)
        for k in range(len(value_list)):
            n=[]
            for j in range(3, len(mergelist[i]), 3):
                if value_list[k]==mergelist[i][j]:
                    n.append(j)
                else:
                    n=n
            if n!=[]:
                sum=0
                for x in n:
                    sum=sum+int(mergelist[i][int(x)+1])
                lindeltestdatalist.append(sum)
            else:
                lindeltestdatalist.append(0)
        lindeltestdata.append(lindeltestdatalist)
    for i in range(1,len(lindeltestdata)):
        sum=0
        for j in range(2,len(lindeltestdata[i])):
            sum=sum+int(lindeltestdata[i][j])
        if sum==0:
            continue
        else:
            lindeltestdata[i][2:]=[int(x)/sum for x in lindeltestdata[i][2:]]
    lindeltestdata= pd.DataFrame(lindeltestdata)
    lindeltestdata.to_csv('lindeltestdata.csv',index=None,header=None)

if __name__ == '__main__':
    #data transformation
    a=rawdata("result.txt","result1.txt")#forecast data cell_line="K562",dpi="DPI7", coverage="800x"
    rawdata = pd.DataFrame(a)
    rawdata.to_csv('rawdata.csv',index=None,header=None)
    #data cleaning
    forecastdatapath='Supplementarydata1.csv'#forecast supplementarydata1
    b=supplementarydata(forecastdatapath)
    supplementarydata = pd.DataFrame(b)
    supplementarydata.to_csv('supplementarydata.csv',index=None,header=None)

    #Read data
    rawpath1='rawdata.csv'
    rawdatalist1 = []
    with open(rawpath1) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for ll in reader:
            rawdatalist1.append(ll)
    supplementarypath='supplementarydata.csv'
    supplementarylist=[]
    with open(supplementarypath) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for ll in reader:
            supplementarylist.append(ll)

    #Corresponding CROTON training set and test set
    crotondatapath='crotondata.csv'
    crotondata=[]
    with open(crotondatapath) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for ll in reader:
            crotondata.append(ll)
    crotonlist=[]
    for i in range(len(crotondata)):
        crotonlist.append(crotondata[i][0])
    supplementary=[]
    for i in range(len(crotonlist)):
        for j in range(len(supplementarylist)):
            if crotonlist[i]==supplementarylist[j][0][3:]:
                supplementary.append(supplementarylist[j])

    #merge data
    mergedata=merge(supplementary,rawdatalist1)
    mergedata = pd.DataFrame(mergedata)
    mergedata.to_csv('mergedata.csv',index=None,header=None)

    #read data
    mergepath='mergedata.csv'
    mergelist=[]
    with open(mergepath) as f:
        for line in f:
            ll = line.strip()
            ll = ll.rstrip(',')
            mergelist.append(ll.split(","))

    #convert the CIGAR strings
    mergelist=transforlabel(mergelist)
    #processed data
    processeddata=comparisondata(mergelist)

