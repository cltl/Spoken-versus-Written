from collections import defaultdict

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

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
            flickr_index[identifier].append(description + '\n')

descriptions = [flickr_index[imgid] for imgid in train_ids]
flattened_descriptions = [description for split in zip(*descriptions)
                                      for description in split]

gen = chunks(flattened_descriptions, 1000)
for i in range(100):
    lines = next(gen)
    with open('./Resources/Flickr30K/train_chunks/flickr_chunk.{0:03}'.format(i), 'w') as f:
        f.writelines(lines)
