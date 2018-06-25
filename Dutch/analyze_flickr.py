# Here's how to run our analysis for Flickr30K.

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

files = glob.glob('./Resources/Written-descriptions/Flickr30K-Val/val*')

parallel_flickr = [get_lines(filename) for filename in files]
all_flickr = [desc for paralist in parallel_flickr for desc in paralist]

results = dict(lengths=get_lengths(all_flickr),
               words=linguistic_metrics(all_flickr),
               msttr=dict(all=msttr(all_flickr),
                          parallel=np.mean([msttr(descriptions) for descriptions in parallel_flickr])
                          )
                )

with open('./Results/flickr_results.json','w') as f:
    json.dump(results, f)
