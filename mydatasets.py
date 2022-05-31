from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision import transforms
import numpy as np
import pickle
import os

class Afad_Dataset(Dataset):
    def __init__(self, type, fold, transform, K):
        assert os.path.exists('datasets/AFAD-Full'), 'Run datasets/prepare_afad.py'
        self.files = sorted([(r, f) for r, _, fs in os.walk('datasets/AFAD-Full') for f in fs])
        # I am assuming there are 10 folds
        nfolds = 10
        rand = np.random.RandomState(123)
        ix = rand.choice(len(self.files), len(self.files), False)
        tr_ix = np.concatenate((ix[:fold*len(self.files)//nfolds], ix[(fold+1)*len(self.files)//nfolds:]))
        ts_ix = ix[fold*len(self.files)//nfolds:(fold+1)*len(self.files)//nfolds]
        self.X = [None] * len(self.files)
            
        self.Y = [int(r.split('/')[-2]) for r, f in self.files]
        self.transform = transform

    def len_nclasses(self):
        return np.max(self.Y)+1

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        if self.X[i] is None:
            fname = os.path.join(*self.files[i])
            self.X[i] = read_image(fname)
            self.X[i] = self.X[i].float()
        return self.X[i], self.Y[i]

class Herlev_Dataset(Dataset):
    def __init__(self, type, fold, transform, K):
        assert os.path.exists('datasets/herlev'), 'Run datasets/prepare_Herlev.py'
        assert K is not None, 'K must be defined for Herlev'
        self.X, self.Y = pickle.load(open(f'data/herlev/k{K}.pickle', 'rb'))[fold][type]
        self.transform = transform

    def len_nclasses(self):
        return np.max(self.Y)+1

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        X = self.transform(self.X[i])
        Y = self.Y[i]
        return X, Y


class FocusPath_Dataset(Dataset):
    def __init__(self, type, fold, transform, K):
        assert os.path.exists('datasets/FocusPath'), 'Run datasets/prepare_FocusPath.py'
        assert K is not None, 'K must be defined for FocusPath: 12'
        self.X, self.Y = pickle.load(open(f'data/FocusPath/k{K}.pickle', 'rb'))[fold][type]
        self.transform = transform


    def len_nclasses(self):
        return np.max(self.Y)+1

    def __len__(self):
        return len(self.X)
        
            def __getitem__(self, i):
        X = self.transform(self.X[i])
        Y = self.Y[i]
        return X, Y


aug_transforms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomAffine(180, (0, 0.1), (0.9, 1.1)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.ColorJitter(saturation=(0.5, 2.0)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

val_transforms = transforms.Compose([
    transforms.ToTensor(),  
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])