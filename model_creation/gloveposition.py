#coding=utf-8
# from util import logTool, util
import numpy as np
import gc
import pandas as pd

# Dictionary generation based on K
def dnaListGet(dnaList, k):
    tempList = []
    if dnaList:
        for item in dnaList:
            itemA = item + "A"
            tempList.append(itemA)
            itemT = item + "T"
            tempList.append(itemT)
            itemC = item + "C"
            tempList.append(itemC)
            itemG = item + "G"
            tempList.append(itemG)
    else:
        tempList.append("A")
        tempList.append("T")
        tempList.append("C")
        tempList.append("G")
    if k > 1:
        tempList = dnaListGet(tempList, k - 1)
    return tempList

def getDNA(dic, index):
    if index < len(dic):
        return dic[index]
    else:
        ind = 0
        res = ""
        while ind < len(dic[0]):
            res = res + "Q"
            ind = ind + 1
        print("The index“%s”you are looking for does not exist. Convert it to %s" % (index, res))
        return res


# Get index from DNA
def getIndex(dic, item):
    if item in dic:
        return dic.index(item)
    else:
        print("The DNA“%s”you're looking for doesn't exist. Convert it to %s" % (item, len(dic)))
        return len(dic)


# Generate "position_data_3_1.txt"
def genposidata(KMER, KSTEP):
    dataPath = 'data/data.csv'
    outputList = "data/position_data_%s_%s.txt" % (KMER, KSTEP)
    M = int((60 - KMER) / KSTEP + 1)
    dic = dnaListGet([], KMER)
    dataList = []
    print('loading data')
    with open(dataPath) as f:
        for line in f:
            ll = line.strip()
            dataList.append(ll.split(","))

    fout = open(outputList, 'w')
    for i in range(len(dataList)):
        inputFlag = 0
        index = 0
        kmerList = [','.join(dataList[i][0:557])]

            # kmer列表
        while index + KMER <= len(dataList[i][557]):
            windData = dataList[i][557][index:index + KMER].upper()
            ind = getIndex(dic, windData)
            if ind < len(dic):
                kmerList.append(ind*M+int(index/KSTEP))
            else:
                inputFlag = 1
                break
            index += KSTEP
        fout.writelines(",".join('%s' % item for item in kmerList) + '\n')
    del dic,dataList
    gc.collect()
    return kmerList

def genposiglove(KMER,KSTEP,coWindow,XMAX,N):
    #Generate word vector matrix of glove + position
    tableSize = 4 ** KMER
    N=int(N)
    M = int((60 - KMER) / KSTEP + 1)
    wordvectorsize=tableSize*M
    GloVeVecmatrix = np.loadtxt(open("data/Datakeras_GloVeVec_data_%s_%s_%s_%s_%s_20000.csv"%(KMER,KSTEP,coWindow,XMAX,N),"rb"),delimiter=",",skiprows=0)
    positionalmatrix = np.loadtxt(open('data/position_%s_%s_%s.csv'%(KMER,KSTEP,N),"rb"),delimiter=",",skiprows=0)
    glovepositionmatrix = []
    for i in range(wordvectorsize):
        glovepositionmatrix.append(GloVeVecmatrix[i//M]+positionalmatrix[i%M])
    glovepositionmatrix = pd.DataFrame(glovepositionmatrix)
    glovepositionmatrix.to_csv('data/glovepositionmatrix_%s_%s_%s_%s_%s.csv'%(KMER,KSTEP,coWindow,XMAX,N), header=None)
    return glovepositionmatrix

