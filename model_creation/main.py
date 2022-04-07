#coding=utf-8
from __future__ import print_function
import numpy as np
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.optimizers import Adam,Adadelta,Nadam
import gc
from keras.preprocessing.sequence import pad_sequences
from loadData import loadGlove, loadData
from model_get import modelSelection
from keras.callbacks import ReduceLROnPlateau,EarlyStopping


def smallmodel(KMER,KSTEP,coWindow,XMAX,N,BATCH_SIZE,NUM_EPOCHS,p,m,n,nummodel,lamuda,units):
    # network and training
    VERBOSE = 1#Show progress bar
    OPTIMIZER = Adam(lr=10e-4)
    tableSize = 4 ** KMER
    N=int(N)
    M = int((60 - KMER) / KSTEP + 1)
    VOCAB_SIZE=tableSize*M
    EMBED_SIZE = N
    BATCH_SIZE = BATCH_SIZE
    NUM_EPOCHS = NUM_EPOCHS
    MODEL_select = int(nummodel)

    glove_inputpath = 'data/glovepositionmatrix_%s_%s_%s_%s_%s.csv'%(KMER,KSTEP,coWindow,XMAX,N)
    data_inputpath = "data/position_data_%s_%s.txt" % (KMER, KSTEP)


    # load GloVe model
    model_glove = loadGlove(glove_inputpath)
    embedding_weights = np.zeros((VOCAB_SIZE, EMBED_SIZE))
    for i in range(VOCAB_SIZE):
        embedding_weights[i, :] = model_glove[str(i)]
    print('GloVe model loaded')


    # loadData
    data, label = loadData(data_inputpath)
    X = padded_docs = pad_sequences(data)
    X_forecast=X[0:35129]
    X_lindel=X[35129:35569]
    X_sprout=X[35569:]
    Y = padded_docs = pad_sequences(label,dtype='float32')
    Y_forecast=Y[0:35129]
    Y_lindel = Y[35129:35569]
    Y_sprout=Y[35569:]

    X_test = X_forecast[0:3512]
    X_valid = X_forecast[3512:7024]
    X_train = X_forecast[7024:]
    Y_test = Y_forecast[0:3512]
    Y_valid = Y_forecast[3512:7024]
    Y_train = Y_forecast[7024:]

    # model
    model = Sequential()
    model.add(Embedding(VOCAB_SIZE, EMBED_SIZE,input_length=M,
                        weights=[embedding_weights],
                        trainable=True))
    model, model_message = modelSelection(model, MODEL_select,KMER,KSTEP,N,lamuda,units)
    model.summary()
    print("model loaded")
    print(model_message)
    model.compile(loss='categorical_crossentropy',
                  optimizer=OPTIMIZER, metrics=['mse'])
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=p, patience=m)
    early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=n, verbose=1)
    model.fit(X_train, Y_train, batch_size=BATCH_SIZE,
                        epochs=NUM_EPOCHS,
                        validation_data=(X_valid, Y_valid), verbose=VERBOSE, callbacks=[reduce_lr,early_stopping])
 
    Y_pred = model.predict(X_test)
    Y_sproutpred=model.predict(X_sprout)
    Y_lindelpred=model.predict(X_lindel)

    del embedding_weights,model_glove,data,label,X,X_test
    gc.collect
    return Y_test,Y_pred,Y_sprout,Y_sproutpred,Y_lindel,Y_lindelpred


