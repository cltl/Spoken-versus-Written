# Here's how to run our analysis for MS COCO.

# Import the relevant functions.
from EN_spoken_vs_written import preprocess, get_lengths, linguistic_metrics, msttr

# Installed module.
import numpy as np

# Stdlib
import json
from collections import defaultdict

# Compile index for the written MS COCO descriptions
coco_index = defaultdict(list)
with open("./Resources/MSCOCO/captions_train2014.json") as f:
    data = json.load(f)
    for entry in data['annotations']:
        image_id = entry['image_id']
        description = entry['caption']
        tokens = preprocess(description)
        coco_index[image_id].append(tokens)

all_coco = [desc for desc_list in coco_index.values() for desc in desc_list]
parallel_coco = list(zip(*coco_index.values()))

results = dict(lengths=get_lengths(all_coco),
               words=linguistic_metrics(all_coco),
               msttr=dict(all=msttr(all_coco),
                          parallel=np.mean([msttr(descriptions) for descriptions in parallel_coco])
                          )
                )

with open('./Results/coco_results.json','w') as f:
    json.dump(results, f)
