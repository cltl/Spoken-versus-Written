# Here's how to run our analysis for DIDEC.

# Import the relevant functions.
from NL_spoken_vs_written import preprocess, get_lengths, linguistic_metrics, msttr

# Installed module.
import numpy as np

# Stdlib
import json
import glob
from collections import defaultdict

# Only focus on the Validation data.

def get_lines(filename):
    with open(filename) as f:
        return [preprocess(line.strip()) for line in f]

files = glob.glob('./Resources/Spoken-descriptions/DIDEC-plain/descriptions*.txt')

parallel_didec = [get_lines(filename) for filename in files]
all_didec = [desc for paralist in parallel_didec for desc in paralist]

results = dict(lengths=get_lengths(all_didec),
               words=linguistic_metrics(all_didec),
               msttr=dict(all=msttr(all_didec),
                          parallel=np.mean([msttr(descriptions) for descriptions in parallel_didec])
                          )
                )

with open('./Results/didec_results.json','w') as f:
    json.dump(results, f)
