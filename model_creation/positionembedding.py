#coding=utf-8
# Positional Encoding

import math
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable


class PositionalEncoding(nn.Module):

    def __init__(self, d_model, dropout, max_len=5000):
        super(PositionalEncoding, self).__init__()

        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)

        position = torch.arange(0., max_len).unsqueeze(1)

        div_term = torch.exp(torch.arange(0., d_model, 2) *

                             -(math.log(10000.0) / d_model))

        pe[:, 0::2] = torch.sin(position * div_term)  

        pe[:, 1::2] = torch.cos(position * div_term) 

        pe = pe.unsqueeze(0)  # [1, max_len, d_model]

        self.register_buffer('pe', pe)


    def forward(self, x):
        x = x + Variable(self.pe[:, :x.size(1)], requires_grad=False)

        return self.dropout(x)

def posidata(KMER,KSTEP,N):
    N=int(N)
    M = int((60 - KMER) / KSTEP + 1)
    pe = PositionalEncoding(N, 0)
    y = pe.forward(Variable(torch.zeros(1, M, N)))
    y = torch.squeeze(y)
    y = np.transpose(y.numpy(), (0, 1))
    y = pd.DataFrame(y)
    y.to_csv('data/position_%s_%s_%s.csv'%(KMER,KSTEP,N), index=None, header=None)
    return y



