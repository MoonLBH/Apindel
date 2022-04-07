#coding=utf-8
# from util import logTool, util
import random
import numpy as np
from mittens import GloVe
import gc
import pandas as pd
from util import util as use


# Calculation of co-occurrence matrix
def countCOOC(cooccurrence, window, coreIndex):
    for index in range(len(window)):
        if index == coreIndex:
            continue
        else:
            cooccurrence[window[coreIndex]][window[index]
                                            ] = cooccurrence[window[coreIndex]][window[index]] + 1
    return cooccurrence

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

# Get DNA according to index
def getDNA(dic, index):
    if index < len(dic):
        return dic[index]
    else:
        ind = 0
        res = ""
        while ind < len(dic[0]):
            res = res + "Q"
            ind = ind + 1
        print("The index “%s” you are looking for does not exist. Convert it to %s" % (index, res))
        return res

# Get index from DNA
def getIndex(dic, item):
    if item in dic:
        return dic.index(item)
    else:
        print("The DNA “%s” ou're looking for doesn't exist. Convert it to %s" % (item, len(dic)))
        return len(dic)


#Generate data with index of KMER and kstep
def Indexdata(KMER,KSTEP):
    dic = dnaListGet([], KMER)
    dataPath = 'data/data.csv'
    outputList = "data/data_%s_%s.txt"%(KMER,KSTEP)
    # 读取数据
    dataList = []
    print('loading data')
    with open(dataPath) as f:
        for line in f:
            ll = line.strip()
            dataList.append(ll.split(","))
    dataList=dataList[0:35129]
    print('shuffling data')
    random.seed(50)
    random.shuffle(dataList)
    # kmer cal
    kmerListAll = []
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
                kmerList.append(ind)
            else:
                inputFlag = 1
                break
            index += KSTEP
        fout.writelines(",".join('%s' % item for item in kmerList) + '\n')

        # 写入临时表
        kmerListAll.append(kmerList)

        if i % 500 == 0:
            print("已经处理了%s条数据" % (i))
    fout.close()
    del dic,dataList,kmerList
    gc.collect()
    print("序列已经转化为向量,用时处理了%s条数据" % (i))
    data = kmerListAll
    return data,kmerListAll



#Generate co-occurrence matrix
def cooccurrencearray(KMER,KSTEP,coWindow):
    # Build an empty Thesaurus
    tableSize = 4 ** KMER
    cooccurrence = np.zeros((tableSize, tableSize), "int64")
    print("Construction of empty thesaurus completed")

    # Start statistics
    flag = 0
    window = []
    M=int((60-KMER)/KSTEP+2)
    data, kmerListAll = Indexdata(KMER, KSTEP)
    for item in data:
        itemInt = [int(x) for x in item[1:M]]
        for core in range(0, len(item[1:M])):
            if core <= coWindow:
                # Insufficient left window
                window = itemInt[0:core + coWindow + 1]
                coreIndex = core
                cooccurrence = countCOOC(cooccurrence, window, coreIndex)
            elif core >= len(item[1:M]) - 1 - coWindow:
                # Insufficient right window
                window = itemInt[core - coWindow:len(item[1:M])]
                coreIndex = coWindow
                cooccurrence = countCOOC(cooccurrence, window, coreIndex)

            else:
                # No problem left or right
                window = itemInt[core - coWindow:core + coWindow + 1]
                coreIndex = coWindow
                cooccurrence = countCOOC(cooccurrence, window, coreIndex)
        flag = flag + 1
    del data, kmerListAll, window
    gc.collect()
    coocPath = "data/Datacooccurrence_data_%s_%s_%s.csv"%(KMER,KSTEP,coWindow)
    writer = use.csvWrite(coocPath)
    for item in cooccurrence:
        writer.writerow(item)
    print("Co-occurrence matrix export completed" )
    return cooccurrence



# GloVe
def glove(KMER,KSTEP,coWindow,XMAX,N):
    print("Start Glove calculation")
    cooccurrence = cooccurrencearray(KMER, KSTEP, coWindow)
    coocMatric = np.array(cooccurrence, "float32")
    N=int(N)
    XMAX=int(XMAX)
    # Start iteration
    glove_model = GloVe(n=N, max_iter=20000,
                        display_progress=100, xmax=XMAX)
    embeddings = glove_model.fit(coocMatric)
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_csv('data/Datakeras_GloVeVec_data_%s_%s_%s_%s_%s_20000.csv'%(KMER,KSTEP,coWindow,XMAX,N),index=None, header=None)
    del cooccurrence,coocMatric
    gc.collect()
    return embeddings




