#!/bin/sh
KS="63"
METRICS="wilson mae acc mse"
ARCHITECTURES="mobilenet_v2 resnet18 vgg16"
METHODS="Base OrdinalEncoder CO2 HO2 QUL_CE QUL_HO_pre"
TOCLASSES="mode mode mode mode mode mode"
HEADERS="CE OE CO2 HO2 QUL_CE QUL_HO"


echo "Results tables..."
for METRIC in $METRICS; do
    for K in $KS; do
        echo $METRIC $K
        python3 evaluate.py $METRIC $K *.txt \
            --architectures $ARCHITECTURES \
            --methods $METHODS \
            --toclasses $TOCLASSES \
            --headers $HEADERS \
            > results-$METRIC-$K.tex
    done
done



#mv results-mae-7.tex table4.tex
#mv results-mae-4.tex table5.tex
#mv results-acc-7.tex table6.tex
#mv results-acc-4.tex table7.tex
#mv results-wilson-7.tex table8.tex
#mv results-wilson-4.tex table9.tex
#mv results-tau-7.tex tableA1.tex
#mv results-tau-4.tex tableA2.tex
#mv results-toclass-7.tex tableA3.tex
#mv results-toclass-4.tex tableA4.tex

