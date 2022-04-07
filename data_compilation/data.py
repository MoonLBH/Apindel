# -*- coding: utf-8 -*-

import time
import pandas as pd
import csv


def get_data(df,lindel):
    seq = 'TAACGTTATCAACAGCTCACCAGATACGGGATACGGTTGAACTGCGTGGATCAATGCGTC'
    sequence1 = df.reindex(columns=['Column' + '1'])
    label1=df.reindex(columns=['Column' + str(x) for x in range(2, 559)])
    sequence2 = lindel.reindex(columns=['Column' + '1'])
    label2=lindel.reindex(columns=['Column' + str(x) for x in range(2, 559)])
    sequence1 = pd.DataFrame(sequence1)
    label1 = pd.DataFrame(label1)
    sequence2 = pd.DataFrame(sequence2)
    for i in range(sequence2.shape[0]):
        sequence2.iloc[i, 0]=seq.replace('AGCTCACCAGATACGGGATA',sequence2.iloc[i, 0])
    label2= pd.DataFrame(label2)
    data1=pd.concat([label1, sequence1], axis=1)
    data2=pd.concat([label2, sequence2], axis=1)
    data=pd.concat([data1, data2], axis=0)
    return data


if __name__ == '__main__':
    strt_tm = time.time()

    df = pd.read_excel('data/forecastnewnew.xlsx')#the result of compile_forecast.py
    lindel= pd.read_excel('data/test.xlsx')#Lindel test data
    data = get_data(df,lindel)
    data = pd.DataFrame(data)
    zero = [['0' for j in range(557)] for i in range(1603)]
    zero = pd.DataFrame(zero, columns=['Column' + str(x) for x in range(2, 559)])
    dataPath = 'D:/R/R_code/6957125/key_df.csv'#sprout test data
    dataList = []
    with open(dataPath) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for ll in reader:
            dataList.append(ll)
    list = []
    for i in range(1, len(dataList)):
        list.append(dataList[i][1])
    zero['Column1'] = list
    data = pd.concat([data, zero], axis=0)
    data.to_csv('data/data.csv', index=None,header=None)
