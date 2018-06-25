import json

with open('./Resources/MSCOCO/captions_train2014.json') as f:
    d = json.load(f)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

gen = chunks(d['annotations'], 1000)
for i in range(100):
    annotations = next(gen)
    lines = [entry['caption']+'\n' for entry in annotations]
    with open('./Resources/MSCOCO/coco_train_chunks/coco_train.{0:03}'.format(i), 'w') as f:
        f.writelines(lines)
