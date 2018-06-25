from scipy.stats import kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
import numpy as np

from itertools import repeat
import json

def load_json(filename):
    "Load a JSON file and return its contents."
    with open(filename) as f:
        data = json.load(f)
    return data


def tag_scores(scores, group):
    "Helper function for make_score_array(). Provides scores with given label."
    return list(zip(repeat(group), scores))


def make_score_array(coco, flickr, places):
    "Make a numpy record array for the three groups."
    all_scores = []
    all_scores.extend(tag_scores(coco, 'coco'))
    all_scores.extend(tag_scores(flickr, 'flickr'))
    all_scores.extend(tag_scores(places, 'places'))
    return np.rec.array(all_scores, dtype=[('group', 'S10'), ('score', '<i4')])


def compute_statistics(coco, flickr, places, alpha = 0.05):
    "Compute all stats for a given set of groups."
    kruskal_result = kruskal(coco, flickr, places)
    print('Kruskal result:', kruskal_result)
    if kruskal_result.pvalue < alpha:
        print("Use Tukey pairwise HSD.")
        x = make_score_array(coco, flickr, places)
        y = pairwise_tukeyhsd(x['score'], x['group'], alpha=alpha)
        print(y)
    else:
        print("Not significant. Can't proceed with Tukey.")


coco = load_json('./Results/coco_results.json')
flickr = load_json('./Results/flickr_results.json')
places = load_json('./Results/places_results.json')

def compute_length_stats(coco, flickr, places, kind):
    a = coco['lengths'][kind]
    b = flickr['lengths'][kind]
    c = places['lengths'][kind]
    print('Stats for length:', kind)
    compute_statistics(a, b, c)
    print()


def compute_word_stats(coco, flickr, places, kind):
    a = coco['words'][kind]
    b = flickr['words'][kind]
    c = places['words'][kind]
    print('Stats for length:', kind)
    compute_statistics(a, b, c)
    print()

compute_length_stats(coco, flickr, places, kind='all_syllable_lengths')
compute_length_stats(coco, flickr, places, kind='all_char_lengths')
compute_length_stats(coco, flickr, places, kind='lengths_by_tokens')
compute_length_stats(coco, flickr, places, kind='lengths_by_syllables')

compute_word_stats(coco, flickr, places, kind='num_consciousness')
compute_word_stats(coco, flickr, places, kind='num_self_reference')
compute_word_stats(coco, flickr, places, kind='num_attributives')
