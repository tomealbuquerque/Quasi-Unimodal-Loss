# Quasi-Unimodal Distributions for Ordinal Classification

https://www.mdpi.com/2227-7390/10/6/980

by by Tomé Albuquerque, Ricardo Cruz, Jaime S. Cardoso

## Introduction
Ordinal classification tasks are present in a large number of different domains. However, common losses for deep neural networks, such as cross-entropy, do not properly weight the relative ordering between classes. For that reason, many losses have been proposed in the literature, which model the output probabilities as following a unimodal distribution. This manuscript reviews many of these losses on three different datasets and suggests a potential improvement that focuses the unimodal constraint on the neighborhood around the true class, allowing for a more flexible distribution, aptly called quasi-unimodal loss. For this purpose, two constraints are proposed: A first constraint concerns the relative order of the top-three probabilities, and a second constraint ensures that the remaining output probabilities are not higher than the top three. Therefore, gradient descent focuses on improving the decision boundary around the true class in detriment to the more distant classes. The proposed loss is found to be competitive in several cases.

## Usage

  1. Run datasets\prepare_.....py to generate the data.
  2. Run train.py to train the models you want.
  3. Run evaluate.py to generate results table.

## Code organization
```
Edit me to generate
├── a
│   └── nice
│       └── tree
│           ├── diagram!
│           └── :)
└── Use indentation
    ├── to indicate
    │   ├── file
    │   ├── and
    │   ├── folder
    │   └── nesting.
    └── You can even
        └── use
            ├── markdown
            └── bullets!
```
  * **data:** All the datasets used in this work are publicly available: Herlev dataset—http://mde-lab.aegean.gr/index.php/downloads (accessed on: 5 November 2021); FocusPath dataset—https://zenodo.org/record/3926181#.YPFgluhKjIU (accessed on: 5 November 2021); AFAD dataset—https://github.com/afad-dataset/tarball (accessed on: 10 November 2021).
  * **train.py:** train the different models with the different ordinal losses
    and outputs probabilities.
  * **evaluate.py:** generate latex tables with results using the output
    probabilities.
    
## Citation
If you find this work useful for your research, please cite our paper:
```

@Article{math10060980,
AUTHOR = {Albuquerque, Tomé and Cruz, Ricardo and Cardoso, Jaime S.},
TITLE = {Quasi-Unimodal Distributions for Ordinal Classification},
JOURNAL = {Mathematics},
VOLUME = {10},
YEAR = {2022},
NUMBER = {6},
ARTICLE-NUMBER = {980},
URL = {https://www.mdpi.com/2227-7390/10/6/980},
ISSN = {2227-7390},
DOI = {10.3390/math10060980}
}

```

If you have any questions about our work, please do not hesitate to contact [tome.albuquerque@gmail.com](tome.albuquerque@gmail.com)
