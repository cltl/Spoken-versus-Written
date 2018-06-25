# Here's how to run our analysis for Flickr30K.

# Import the relevant functions.
from EN_spoken_vs_written import preprocess, get_lengths, linguistic_metrics, msttr

# Installed module.
import numpy as np

# Stdlib
import json
from collections import defaultdict

# Only focus on the training data.
with open('./Resources/Flickr30K/splits/train_images.txt') as f:
    train_ids = {line.split('.')[0] for line in f}

# Compile index for the written Flickr30K descriptions
flickr_index = defaultdict(list)
with open('./Resources/Flickr30K/results_20130124.token') as f:
    for line in f:
        identifier, description = line.strip().split('\t')
        identifier = identifier.split('.')[0]
        if identifier in train_ids:
            # Properly tokenize the description.
            tokens = preprocess(description)
            # Add it to the index.
            flickr_index[identifier].append(tokens)



all_flickr = [desc for desc_list in flickr_index.values() for desc in desc_list]
parallel_flickr = list(zip(*flickr_index.values()))

results = dict(lengths=get_lengths(all_flickr),
               words=linguistic_metrics(all_flickr),
               msttr=dict(all=msttr(all_flickr),
                          parallel=np.mean([msttr(descriptions) for descriptions in parallel_flickr])
                          )
                )

with open('./Results/flickr_results.json','w') as f:
    json.dump(results, f)
