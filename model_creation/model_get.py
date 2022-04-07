#coding=utf-8
from __future__ import print_function
from keras.layers import Bidirectional, LSTM, BatchNormalization, GRU
from keras.layers.core import Dense, Activation, Dropout, Flatten
from multy import processing



def modelSelection(model, MODEL_select,KMER,KSTEP,N,lamuda,units):
    model_tmpl = [ 1, 2, 3, 4, 5]
    if MODEL_select == model_tmpl[0]:
        return model1(model,KMER,KSTEP,N,lamuda,units)
    if MODEL_select == model_tmpl[1]:
        return model2(model,KMER,KSTEP,N,lamuda,units)
    if MODEL_select == model_tmpl[2]:
        return model3(model,KMER,KSTEP,N,lamuda,units)


#best model
def model1(model_ini,KMER,KSTEP,N,lamuda,units):
    print("model1 loaded with 1 biLSTM, 1 Attention and 2 dense")
    model_message = "l2, biLSTM, Attention, Dense[1024,557]"
    model = model_ini
    # model.add(Dropout(p))

    M = int((60 - KMER) / KSTEP + 1)
    N = int(N)

    firstbilstmlayer=Bidirectional(LSTM(units, input_shape=(M, N), return_sequences=True,activation='relu'))
    model.add(firstbilstmlayer)
    model.add(BatchNormalization())

    head_att_1=Dense(units=units*2)
    model.add(head_att_1)
    model.add(Activation('tanh',name="att_out1"))
    model.add(Dense(units=1,name='att_out2'))
    head_att_2 = Activation('softmax',name="att_out")
    model.add(head_att_2)



    mul_output=processing(x=firstbilstmlayer.output)
    model.add(mul_output)

    model.add(Flatten())
    model.add(Dense(units=1024))
    model.add(Activation('relu'))

    model.add(Dense(units=557))
    model.add(Activation('softmax'))

    return model, model_message

