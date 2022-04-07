# Apindel
A deep learning method for predicting DNA repair outcomes.
## Background
Apindel is a deep learning framework based on Attention mechanism and Positional Encoding for predicting CRISPR/Cas9 repair outcomes.

It automatically trained the sequence features of DNA with GloVe model, introduced location information through Positional Encoding (PE), and embedded the trained word vector matrixes into a deep learning model containing BiLSTM and Attention mechanism.
## Install
* Python == 3.6
* pandas == 1.0.1
* numpy == 1.18.5
* mittens == 0.2
* keras == 2.4.3
* pytorch == 1.7.1
* tensorflow == 2.3.1
## Usage
If you want to reproduce the results of this paper, please perform the following steps：
1、Encode the DNA sequences using the method mentioned in our paper.
