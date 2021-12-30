import argparse
parser = argparse.ArgumentParser()
parser.add_argument('f1')
parser.add_argument('f2')
args = parser.parse_args()

for l1, l2 in zip(open(args.f1), open(args.f2)):
    l1 = ' & '.join(l1.split('&')[:-1])
    l2 = ' & '.join(l2.split('&')[1:-1])
    if l1 and l2:
        print(l1 + l2 + r'\\')
