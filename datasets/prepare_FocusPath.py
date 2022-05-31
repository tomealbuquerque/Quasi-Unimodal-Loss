import numpy as np
import pandas as pd
import cv2
import pickle
import os
import _pickle as cPickle
from sklearn.model_selection import train_test_split, KFold
from sklearn.model_selection import StratifiedKFold


#must download the dataset to FocusPath folder
df=pd.read_excel('FocusPath\DatabaseInfo.xlsx')
labels=df['Subjective Score']
labels=np.array(labels)

#check different labels 
types=np.unique(labels)
df['Subjective Score'].value_counts().sort_index()

file=df['Name']
x_train = []
y_train = []


for idx,filename in enumerate(file):
    if df.iloc[idx]['Subjective Score']!=-10 and df.iloc[idx]['Subjective Score']!=-9 and df.iloc[idx]['Subjective Score']!=-8 and df.iloc[idx]['Subjective Score']!=-7 and df.iloc[idx]['Subjective Score']!=-6 and df.iloc[idx]['Subjective Score']!=-5 and df.iloc[idx]['Subjective Score']!=-4 and df.iloc[idx]['Subjective Score']!=-3 and df.iloc[idx]['Subjective Score']!=-2 and df.iloc[idx]['Subjective Score']!=-1:
        y_train.append(df.iloc[idx]['Subjective Score'])
        path=rf'data\\FocusPath_full\\' + filename
        pre, ext = os.path.splitext(path)
        path=pre + '.png'
        im = cv2.imread(path)
        imnew=cv2.resize(im,(224,224))*255
        x_train.append(imnew)
        print("Remain...",len(file)-idx)


y_train = np.array(y_train)
x_train= np.array(x_train)


#change labels from  0 -> 11

for i in range(len(y_train)):
    if y_train[i]==12 or y_train[i]==13 or y_train[i]==14:
        y_train[i]=11


y_train_subj = np.array(y_train, np.uint8)


X = np.array(x_train, np.uint8)
Y = np.array(y_train_subj, np.uint8)

# kfold
state = np.random.RandomState(1234)
kfold = StratifiedKFold(10, shuffle=True, random_state=state)
folds = [{'train': (X[tr], Y[tr]), 'test': (X[ts], Y[ts])} for tr, ts in kfold.split(X, Y)]
pickle.dump(folds, open(f'FocusPath/k12.pickle', 'wb'))
