import json
import spacy
from collections import Counter
from tabulate import tabulate

nlp = spacy.load('en', disable=['ner','parser'])

def tokenize(sentence):
    return [tok.orth_.lower() for tok in nlp.tokenizer(sentence)]

def nominalization(word):
    return word[-4:] in {'tion', 'ment', 'ness'} or word[-3:] == 'ity'

def get_nouns(sentence):
    doc = nlp(sentence)
    return [tok.orth_ for tok in doc if tok.pos_ == 'NOUN']

################################################################################
# Init vocab

vocab = set()

################################################################################
# Flickr
flickr_counter = Counter()
with open('./Resources/Flickr30K/results_20130124.token') as f:
    for line in f:
        tokens = line.lower().split()[1:]
        sentence = ' '.join(tokens)
        flickr_counter.update(get_nouns(sentence))

print('Flickr30K')
print(flickr_counter.most_common(10))
print()

################################################################################
# Places

places_counter = Counter()
with open('./Resources/Places/metadata/utt2ASR') as f:
    for line in f:
        identifier, *tokens = line.lower().strip().split()
        sentence = ' '.join(tokens)
        places_counter.update(get_nouns(sentence))

print('Places')
print(places_counter.most_common(10))
print()

################################################################################
# MS COCO

coco_counter = Counter()
with open("./Resources/MSCOCO/captions_train2014.json") as f:
    data = json.load(f)
    for entry in data['annotations']:
        description = entry['caption']
        coco_counter.update(get_nouns(description))

print('MS COCO')
print(coco_counter.most_common(10))
print()

noun_counts = dict(coco=coco_counter,
                   flickr=flickr_counter,
                   places=places_counter)

with open('noun_counts.json','w') as f:
    json.dump(noun_counts, f)

def get_rows(n):
    rows = []
    for i, pairs in enumerate(zip(flickr_counter.most_common(n),
                                  coco_counter.most_common(n),
                                  places_counter.most_common(n)),
                              start=1):
        row = [i] + [value for pair in pairs for value in pair]
        rows.append(row)
    return rows

rows = get_rows(25)
headers = ['#', 'Word', 'Count', 'Word', 'Count', 'Word', 'Count']
table = tabulate(rows, headers, tablefmt='latex_booktabs')
print(table)
