import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--dataset', choices=['herlev', 'afad', 'focuspath'], default='afad')
parser.add_argument('metric')
parser.add_argument('K', type=int)
parser.add_argument('outputs', nargs='+')
parser.add_argument('--architectures', nargs='+')
parser.add_argument('--methods', nargs='+')
parser.add_argument('--toclasses', nargs='+', choices=['mode', 'mean', 'median'])
parser.add_argument('--headers', nargs='+')
args = parser.parse_args()

import numpy as np
import pickle
import mydatasets, mymetrics
from scipy import stats
import os
from torch.utils.data import Dataset, DataLoader, Subset

def escape(s):
    return s.replace('_', f'\_')

#YY = [pickle.load(open(f'data/k12.pickle', 'rb'))[fold]['test'][1] for fold in range(10)]
ds = getattr(mydatasets, f'{args.dataset.title()}_Dataset')
ts_ds = ds('test', 0, mydatasets.val_transforms, args.K)
ts = DataLoader(ts_ds, 1, pin_memory=True)
YY=[]
for _, Y in ts:
    YY.append(Y)

print('classes:', len(np.unique(YY)))


metric = getattr(mymetrics, args.metric)
order, magnitude, places, proba = mymetrics.properties[args.metric]

architectures = args.architectures if args.architectures else sorted({os.path.basename(out).split('-')[4] for out in args.outputs})
methods = args.methods if args.methods else sorted({os.path.basename(out).split('-')[6] for out in args.outputs})

fields = args.outputs[0][:-4].split('-')[1:-1]
fields = {k: v for k, v in zip(fields[::2], fields[1::2])}

print(r'''\documentclass{standalone}
\begin{document}''')
print('\\begin{tabular}{l' + ('r'*len(methods)) + '}')
print('& ' + ' & '.join(map(escape, args.headers if args.headers else methods)) + '\\\\\\hline')

sum_avgs = []
winners = [0] * len(methods)

# for architecture in architectures:
    # print('\\textbf{%s}' % escape(architecture), end=' & ')
    # avgs = []
    # devs = []
    # scores_per_fold = []
    # for i, method in enumerate(methods):
        # toclass = args.toclasses[i] if args.toclasses else 'mode'
        # scores = mymetrics.evaluate(YY, args.K, args.outputs, proba, architecture, method, metric, toclass)
        # scores_per_fold.append(scores)
        # avgs.append(np.mean(scores))
        # devs.append(np.std(scores))
    # best = getattr(np, 'nanarg' + order)(avgs)
    # for i, (avg, dev) in enumerate(zip(avgs, devs)):
        # print('$', end='')
        # italic = bold = False
        # if i == best:
            # bold = True
        # else:
            # # compare this method against the best using a statistical test
            # this_folds = scores_per_fold[i]
            # best_folds = scores_per_fold[best]
            # _, pvalue = stats.ttest_rel(this_folds, best_folds)
            # italic = pvalue/2 > 0.10  # divide by two to make it one-sided
        # if bold:
            # print(r'\mathbf{', end='')
        # if italic:
            # print(r'\mathit{', end='')
        # print(f'{avg*magnitude:.{places}f} \pm {dev*magnitude:.{places}f}', end='')
        # #print(f'{avg*magnitude:.{places}f}', end='')
        # if bold or italic:
            # print('}', end='')
        # print('$', end='')
        # if i < len(avgs)-1:
            # print(' & ', end='')
        # winners[i] += int(bold)
    # print(' \\\\')
    # sum_avgs.append(avgs)
# print('\\hline')
# print('\\textbf{Avg} & ' + ' & '.join([f'{a*magnitude:.{places}f}' for a in np.mean(sum_avgs, 0)]) + '\\\\')
# print('\\textbf{Winners} & ' + ' & '.join(str(w) for w in winners) + '\\\\')
# print(r'''\end{tabular}
# \end{document}''')
for architecture in architectures:
    print('\\textbf{%s}' % escape(architecture), end=' & ')
    avgs = []
    devs = []
    scores_per_fold = []
    for i, method in enumerate(methods):
        toclass = args.toclasses[i] if args.toclasses else 'mode'
        scores = mymetrics.evaluate(YY, args.K, args.outputs, proba, architecture, method, metric, toclass)
        scores_per_fold.append(scores)
        avgs.append(np.mean(scores))
        devs.append(np.std(scores))
    best = getattr(np, 'nanarg' + order)(avgs)
    for i, (avg, dev) in enumerate(zip(avgs, devs)):
        print('$', end='')
        italic = bold = False
        if i == best:
            bold = True
        else:
            # compare this method against the best using a statistical test
            this_folds = scores_per_fold[i]
            best_folds = scores_per_fold[best]
            _, pvalue = stats.ttest_rel(this_folds, best_folds)
            italic = pvalue/2 > 0.10  # divide by two to make it one-sided
        if bold:
            print(r'\mathbf{', end='')
        if italic:
            print(r'\mathit{', end='')
        print(f'{avg*magnitude:.{places}f} \pm {dev*magnitude:.{places}f}', end='')
        if bold or italic:
            print('}', end='')
        print('$', end='')
        if i < len(avgs)-1:
            print(' & ', end='')
        winners[i] += int(bold)
    print(' \\\\')
    sum_avgs.append(avgs)
print('\\hline')
print('\\textbf{Avg} & ' + ' & '.join([f'{a*magnitude:.{places}f}' for a in np.mean(sum_avgs, 0)]) + '\\\\')
print('\\textbf{Winners} & ' + ' & '.join(str(w) for w in winners) + '\\\\')
print(r'''\end{tabular}
\end{document}''')
