from skimage.io import imread, imsave
from skimage.transform import resize
import numpy as np
import os
os.system("git clone https://github.com/afad-dataset/tarball.git")
os.system("cat tarball/AFAD-Full.tar.xz* > AFAD-Full.tar.xz")
os.system("tar xvf AFAD-Full.tar.xz")
for root, dirs, files in os.walk("AFAD-Full"):
    print(root)
    for fname in files:
        if not fname.endswith('.jpg'):
            continue
        fname = os.path.join(root, fname)
        img = imread(fname)
        if img.shape[0] >= 64 and img.shape[1] >= 64:
            img = resize(img, (224, 224), order=3, preserve_range=True).astype(np.uint8)
            imsave(fname, img, check_contrast=False)
        else:
            os.remove(fname)
os.system("rm -rf tarball AFAD-Full/AFAD-Full.txt AFAD-Full/README.md AFAD-Full/*/*/Thumbs.db")
