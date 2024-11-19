import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import time
import sys
import os

n = len(sys.argv) # check command-line arguments
if n != 2:
  print(f'usage: {sys.argv[0]} <n_CPU>')
  sys.exit()
n_CPU = int(sys.argv[1])

print(f'Using n_CPU={n_CPU} of os.cpu_count()={os.cpu_count()} available CPUs.')

# n_samples= 10000 gives a 1-job time of about 2 seconds.
# n_samples=100000 gives a 1-job time of about 30 seconds; total 2 minutes.
X, y = make_classification(n_samples=10000, n_features=10,
                           n_informative=7, n_redundant=3, random_state=0)

times = np.zeros(shape=n_CPU+1) # ignore position [0]
numbers_of_CPUs = 1 + np.arange(start=0, stop=n_CPU)
for n_jobs in numbers_of_CPUs:
  clf = RandomForestClassifier(n_estimators=100, n_jobs=n_jobs)
  start = time.time()
  clf.fit(X, y)
  end = time.time()
  times[n_jobs] = end - start
  print(f'n_jobs={n_jobs}, clf.fit() took {times[n_jobs]:.3} seconds.')

print(pd.DataFrame({'n_jobs': numbers_of_CPUs, 'time': times[1:]}))
