import json
import spacy
from collections import Counter

nlp = spacy.load('en')

def tokenize(sentence):
    return [tok.orth_.lower() for tok in nlp.tokenizer(sentence)]

def nominalization(word):
    return word[-4:] in {'tion', 'ment', 'ness'} or word[-3:] == 'ity'

################################################################################
# Flickr

# c = Counter()
# with open('./Resources/Flickr30K/results_20130124.token') as f:
#     for line in f:
#         tokens = line.lower().split()[1:]
#         c[tuple(tokens[:2])] += 1
#
# print('Flickr30K')
# print(c.most_common(10))
# print()

################################################################################
# Places

c = Counter()
with open('./Resources/Places/metadata/utt2ASR') as f:
    for line in f:
        identifier, *tokens = line.lower().strip().split()
        str_description = ' '.join(tokens)
        if all([not str_description.startswith('there'),
                not str_description.startswith('this'),
                not str_description.startswith('picture'),
                not str_description.startswith('a picture'),
                not str_description.startswith('photograph'),
                not str_description.startswith('a photograph'),
                ]):
            c[tuple(tokens[:2])] += 1

print('Places')
print(c.most_common(10))
print()

################################################################################
# MS COCO

# c = Counter()
# with open("./Resources/MSCOCO/captions_train2014.json") as f:
#     data = json.load(f)
#     for entry in data['annotations']:
#         description = entry['caption']
#         tokens = tokenize(description)
#         c[tuple(tokens[:2])] += 1
#
# print('MS COCO')
# print(c.most_common(10))
