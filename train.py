import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dataset', choices=['Herlev', 'FocusPath' 'Afad'], default='Afad')
parser.add_argument('architecture', choices=['alexnet', 'densenet161',
    'googlenet', 'inception_v3', 'mnasnet1_0', 'mobilenet_v2', 'resnet18',
    'resnext50_32x4d', 'shufflenet_v2_x1_0', 'squeezenet1_0', 'vgg16',
    'wide_resnet50_2'], default='mobilenet_v2')
parser.add_argument('method', choices=[
    'Base', 'Beckham', 'OrdinalEncoder', 'UnimodalCE', 'UnimodalMSE',
    'CO', 'CO2', 'HO2', 'QUL', 'QUL_CE', 'QUL_HO'])
parser.add_argument('fold', type=int, choices=range(3), default=0)
parser.add_argument('K', type=int, default=63)
parser.add_argument('--epochs', type=int, default=100)
parser.add_argument('--batchsize', type=int, default=200)
parser.add_argument('--lr', type=float, default=1e-4)
args = parser.parse_args()

import numpy as np
from time import time
from torch import optim
from torch.utils.data import Dataset, DataLoader, Subset
from sklearn.model_selection import KFold
import torch
import mydatasets, mymodels
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

torch.backends.cudnn.benchmark = True

ds = getattr(mydatasets, f'{args.dataset.title()}_Dataset')
tr_ds = ds('train', args.fold, mydatasets.aug_transforms, args.K)
ts_ds = ds('test', args.fold, mydatasets.val_transforms, args.K)
tr = DataLoader(tr_ds, args.batchsize, True, pin_memory=True, num_workers=4)
ts = DataLoader(ts_ds, args.batchsize, pin_memory=True, num_workers=4)

def test(val):
    model.eval()
    val_avg_acc = 0
    for X, Y in val:
        X = X.to(device)
        Y = Y.to(device, torch.int64)
        Yhat = model(X)
        Khat = model.to_classes(model.to_proba(Yhat), 'mode')
        val_avg_acc += (Y == Khat).float().mean() / len(val)
    return val_avg_acc

def train(tr, val, epochs=args.epochs, verbose=True):
    for epoch in range(epochs):
        if verbose:
            print(f'* Epoch {epoch+1}/{args.epochs}')
        tic = time()
        model.train()
        avg_acc = 0
        avg_loss = 0
        for X, Y in tr:
            X = X.to(device)
            Y = Y.to(device, torch.int64)
            opt.zero_grad()
            Yhat = model(X)
            loss = model.loss(Yhat, Y)
            loss.backward()
            opt.step()
            Khat = model.to_classes(model.to_proba(Yhat), 'mode')
            avg_acc += (Y == Khat).float().mean() / len(tr)
            avg_loss += loss / len(tr)
        dt = time() - tic
        out = ' - %ds - Loss: %f, Acc: %f' % (dt, avg_loss, avg_acc)
        if val:
            model.eval()
            out += ', Test Acc: %f' % test(val)
        if verbose:
            print(out)
        scheduler.step(avg_loss)

def predict_proba(data):
    model.eval()
    Phat = []
    with torch.no_grad():
        for X, _ in data:
            phat = model.to_proba(model(X.to(device)))
            Phat += list(phat.cpu().numpy())
    return Phat


proposal = args.method in ('CO', 'CO2', 'HO2', 'QUL_HO')
prefix = '-'.join(f'{k}-{v}' for k, v in vars(args).items())
OMEGA = 0.05
if proposal:
    # first need to find the best values for alpha
    OMEGA = 0.05
    nfolds = 3
    kfold = KFold(nfolds, shuffle=True)
    lambdas = 10.**np.arange(-5, 0)
    lambdas_eval = np.zeros(len(lambdas))
    for i, (tr_ix, val_ix) in enumerate(kfold.split(tr_ds)):
        _tr = DataLoader(Subset(tr_ds, tr_ix), args.batchsize)
        _val = DataLoader(Subset(tr_ds, val_ix), args.batchsize)
        for j, lambda_ in enumerate(lambdas):
            print(f'** Validation fold {i+1}/{nfolds} - lambda: {lambda_} ({j+1}/{len(lambdas)})')
            model = getattr(mymodels, args.method)(args.architecture, tr_ds.len_nclasses(), lambda_, OMEGA)
            model = model.to(device)
            opt = optim.Adam(model.parameters(), args.lr)
            scheduler = optim.lr_scheduler.ReduceLROnPlateau(opt)
            train(_tr, None, args.epochs//6, False)
            with torch.no_grad():
                for X, Y in _val:
                    X = X.to(device)
                    Y = Y.to(device)
                    #lambdas_eval[j] += model.loss(model(X), Y) / len(_val)
                    lambdas_eval[j] += (model(X).argmax(1) == Y).float().sum().cpu().numpy() / (len(_val)*nfolds)
    bestlambda = lambdas[np.argmax(lambdas_eval)]
    print('** Final model - best lambda:', bestlambda)
    print('Lambdas metrics:', lambdas_eval)
    prefix += f'-bestlambda-{bestlambda}'
    model = getattr(mymodels, args.method)(args.architecture, tr_ds.len_nclasses(), bestlambda, OMEGA)

elif args.method in ('QUL', 'QUL_CE'):
    model = getattr(mymodels, args.method)(args.architecture, tr_ds.len_nclasses(), OMEGA)
    
elif args.method in ('Base', 'Beckham', 'OrdinalEncoder', 'UnimodalCE', 'UnimodalMSE'):
    model = getattr(mymodels, args.method)(args.architecture, tr_ds.len_nclasses())


model = model.to(device)
opt = optim.Adam(model.parameters(), args.lr)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(opt, verbose=True)
train(tr, ts)
np.savetxt('output-' + prefix + '-proba.txt', predict_proba(ts), delimiter=',')
if args.method in ['HO2']:
    torch.save(model, 'output-' + prefix + '-proba.pth')