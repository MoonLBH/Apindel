import numpy as np
import pandas as pd
import gc
def loadGlove(inputpath, outputpath=""):
    data_list = []
    wordEmb = {}
    with open(inputpath) as f:
        for line in f:
            ll = line.strip().split(',')
            ll[0] = str(int(float(ll[0])))
            data_list.append(ll)

            ll_new = [float(i) for i in ll]
            emb = np.array(ll_new[1:], dtype="float32")
            wordEmb[str(int(ll_new[0]))] = emb

    if outputpath != "":
        with open(outputpath) as f:
            for data in data_list:
                f.writelines(' '.join(data))
        # data_list = [float(i) for i in data_list]
    del data_list
    gc.collect
    return wordEmb


def loadData(inputpath):
    data_list = []
    label = []
    with open(inputpath) as f:
        for line in f:
            ll = [i for i in line.strip().split(',')]
            label_item = ll[0:557]
            data_item = ll[557:]
            data_item = [int(i) for i in data_item]
            label_item=[float(i) for i in label_item]
            # for i in label_item:
            #     if i*10 == int(i)*10:
            #         label_item.append(int(i))
            #     else:
            #         label_item.append(float(i))
            data_list.append(data_item)
            # print(label_item)
            label.append(label_item)
    return data_list, label


