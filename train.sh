#!/bin/sh
#example of training cycle
METHODS="CO2 HO2 QUL_CE QUL_HO"
KS="63"
FOLDS=0
ARCHITECTURES="mobilenet_v2"




for A in $ARCHITECTURES; do
    for K in $KS; do
        for M in $METHODS; do
            for F in $FOLDS; do
                python3 -u train.py $A $M $F $K --batchsize 256
            done
        done
    done
done
