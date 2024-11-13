import numpy as np
import pdb

files = ["distances.txt", "distances1.txt", "distances2.txt", "distances0.txt"]

dist_sets = []

for fpath in files:
    with open(fpath) as f:
        v = f.read()
    l = eval(v)
    avg = np.mean(l)
    print(avg)
    dist_sets.append(l)
all_distances = []
for dists in dist_sets:
    all_distances.extend(dists)
nskip = 691
avgs = []
all_distances = np.array(all_distances)
for i in range(0, len(all_distances), nskip):
    block = all_distances[i : i + nskip]
    avg = np.mean(block)
    avgs.append(avg)
print(
    f"std of avgs: {np.std(avgs)} | minmax of avgs: {np.min(avgs)}, {np.max(avgs)}| avgofavg: {np.mean(avgs)}"
)
