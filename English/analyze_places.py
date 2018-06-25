# Here's how to run our analysis for places.

# Import the relevant functions.
from EN_spoken_vs_written import preprocess, get_lengths, linguistic_metrics, msttr

# Stdlib
import json
from collections import defaultdict

# Compile index for the Places utterances.
places_index = dict()
with open('./Resources/Places/metadata/utt2ASR') as f:
    for line in f:
        identifier, *tokens = line.strip().split()
        # Undo split, to turn tokens back into description.
        description = ' '.join(tokens)
        # Properly tokenize the description.
        tokens = preprocess(description)
        places_index[identifier] = tokens

results = dict(lengths=get_lengths(places_index.values()),
               words=linguistic_metrics(list(places_index.values())),
               msttr=msttr(places_index.values()))

with open('./Results/places_results.json','w') as f:
    json.dump(results, f)
