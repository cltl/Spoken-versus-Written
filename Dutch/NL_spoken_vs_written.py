# Installed
import spacy
from spacy import displacy
import pyphen
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Standard library
from collections import Counter, defaultdict
from string import punctuation

################################################################################
# Global variables.

punctuation_set = set(punctuation)
nlp = spacy.load('nl', disable=['ner'])
dic = pyphen.Pyphen(lang='nl')

################################################################################
# Functions

def preprocess(description):
    description = description.lower()
    return [tok.orth_ for tok in nlp.tokenizer(description)
                      if not tok.orth_ in punctuation_set]

###################################
# Length metrics

def get_syllables(word):
    "Split word into syllables."
    word_with_hyphens = dic.inserted(word)
    syllables = word_with_hyphens.split('-')
    return syllables


def num_syllables(word):
    "Return the number of syllables in a word."
    syllables = get_syllables(word)
    return len(syllables)


def get_lengths(descriptions):
    "Get lengths of descriptions."
    length_dict = dict()
    
    length_dict['all_char_lengths'] = []
    length_dict['all_syllable_lengths'] = []
    length_dict['lengths_by_tokens'] = []
    length_dict['lengths_by_syllables'] = []
    for description in descriptions:
        # Get lengths of words in terms of syllables and characters.
        syllable_list = [num_syllables(word) for word in description]
        char_list     = [len(word) for word in description]
        # Add those to the list.
        length_dict['all_syllable_lengths'].extend(syllable_list)
        length_dict['all_char_lengths'].extend(char_list)
        
        # Measure sentence length in tokens and in syllables.
        sentence_length_tok = len(description)
        sentence_length_syl = sum(syllable_list)
        
        # Add those to their respective lists.
        length_dict['lengths_by_tokens'].append(sentence_length_tok)
        length_dict['lengths_by_syllables'].append(sentence_length_syl)
    
    length_dict['num_descriptions']     = len(length_dict['lengths_by_tokens'])
    length_dict['num_tokens']           = sum(length_dict['lengths_by_tokens'])
    
    length_dict['avg_token_length_syll']= np.mean(length_dict['all_syllable_lengths'])
    length_dict['avg_token_length_char']= np.mean(length_dict['all_char_lengths'])
    length_dict['avg_desc_length_syll'] = np.mean(length_dict['lengths_by_syllables'])
    length_dict['avg_desc_length_tok']  = np.mean(length_dict['lengths_by_tokens'])
    
    length_dict['std_token_length_syll']= np.std(length_dict['all_syllable_lengths'])
    length_dict['std_token_length_char']= np.std(length_dict['all_char_lengths'])
    length_dict['std_desc_length_syll'] = np.std(length_dict['lengths_by_syllables'])
    length_dict['std_desc_length_tok']  = np.std(length_dict['lengths_by_tokens'])
    return length_dict


def perform_ttest(d1, d2, key):
    "Wrapper to perform t-test on data from both dictionaries."
    # Use the same sample size
    num_items = min(len(d1[key]),
                    len(d2[key]))
    
    print('items:', num_items)
    # Carry out t-test
    result = ttest_ind(d1[key][:num_items], d2[key][:num_items])
    print(result)


# https://stackoverflow.com/a/312464/2899924
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def msttr(descriptions, n=1000):
    "Mean-segmented type-token ratio"
    tokens = [token for description in descriptions
                    for token in description]
    type_counts = []
    for chunk in chunks(tokens, 1000):
        if len(chunk) == n:
            num_types = len(set(chunk))
            type_counts.append(num_types)
    
    # return the average number of types divided by n.
    return (float(sum(type_counts))/len(type_counts))/n


###################################
# Linguistic metrics.

def attributive_count(doc):
    "Count attributive adjectives in a document."
    attributive_counter = 0
    for tok in doc:
        if all([tok.pos_ == 'ADJ',
                tok.dep_ == 'amod',
                tok.head.pos_ in {'NOUN', 'PROPN'}]):
            attributive_counter += 1
    return attributive_counter


# English
# consciousness_of_projection = {'apparently', 'appear', 'appears',
#                                'certainly', 'clearly', 'definitely',
#                                'likely', 'may','maybe', 'might',
#                                'obviously', 'perhaps', 'possibly',
#                                'presumably', 'probably', 'surely',
#                                'seem', 'seemed', 'seemingly', 'seems'}

consciousness_of_projection = {'lijkt', 'lijken', 'waarschijnlijk', 'misschien',
                               'duidelijk', 'mogelijk', 'zeker'}

# English
# self_reference_words = {'i', 'me', 'my'}
self_reference_words = {'ik', 'me', 'mij'}

# English
# positive_allness = {'all', 'each', 'every'}
positive_allness = {'alle', 'elke', 'iedere', 'iedereen'}

# English
# negations = {'no', 'none', 'not', 'nothing', "n't", 'nobody', 'neither', 'nor', 'never', 'nowhere'}
negations = {'geen', 'niet', 'niemand', 'nergens', 'noch', 'nooit', 'niets'}

# English
# pseudo_quantifiers = {'much', 'many', 'lots', 'few', 'some', 'plenty'}
# pseudo_quantifiers_mwe = {' a lot '}
pseudo_quantifiers = {'veel', 'vele', 'weinig', 'enkele'}
pseudo_quantifiers_mwe = {' een paar ', ' een hoop ', ' grote hoeveelheid ', ' kleine hoeveelheid '}

################################################################################
# TO DO

# English
# pronoun_it = {'it'}

# size = {'gigantic', 'giant', 'enormous', 'immense', 'collossal', 'massive', 'vast',
#         'huge', 'big', 'large', 'small', 'puny', 'teensy', 'tiny', 'miniscule', 'teeny'}

# English
# From Biber, extended with our own.
# downtoners       = {'almost', 'barely', 'fairly', 'hardly', 'merely', 'mildly',
#                     'nearly', 'partially', 'partly', 'practically', 'quite',
#                     'rather', 'relatively', 'scarcely', 'slightly', 'somewhat',
#                     'virtually'}
#
# English
# # From Biber, extended with our own.
# amplifiers       = {'absolutely', 'absurdly', 'altogether', 'amazingly', 'awfully',
#                     'completely', 'deeply', 'downright', 'entirely', 'extremely',
#                     'fully', 'greatly', 'highly', 'intensely', 'perfectly',
#                     'strikingly', 'strongly', 'terribly', 'thoroughly',
#                     'totally', 'unbelievably', 'utterly', 'very'}
#
#
# def nominalization(word):
#     "Identify nominalizations (ending in -tion, -ment, -ness, -ity and their plurals.)"
#     return any([word[-6:] in {'nesses'},
#                 word[-5:] in {'tions', 'ments', 'ities'},
#                 word[-4:] in {'tion', 'ment', 'ness'},
#                 word[-3:] == 'ity'])
#
#
# def num_nominalizations(doc):
#     "Count the number of nominalizations."
#     noms = [tok for tok in doc if nominalization(tok.orth_)]
#     return len(noms)


# Prepositional phrases, approximation:
def num_prepositions(doc):
    "Count the number of prepositions."
    return len([tok for tok in doc if tok.pos_ == 'ADP'])


# Adverbs:
def num_adverbs(doc):
    "Count the number of adverbs."
    return len([tok for tok in doc if tok.pos_ == 'ADV'])


# Predicative adjectives:
# def predicative_count(doc):
#     "Count predicative adjectives in a document."
#     predicative_counter = 0
#     for tok in doc:
#         if all([tok.pos_ == 'ADJ',
#                 tok.dep_ == 'acomp',
#                 tok.head.pos_ == 'VERB']):
#             predicative_counter += 1
#     return predicative_counter


####################
# NOT USED

# These are from Biber, who copied them from Quirk et al. (1985:514ff).
# They are used to "mark situated, as opposed to abstract, textual content."
# This is not so relevant for us, because neither task is situated.
# place_adverbials = {'aboard', 'above', 'abroad', 'ahead', 'alongside', 'around',
#                     'ashore', 'astern', 'away', 'behind', 'below', 'beneath',
#                     'beside', 'downhill', 'downstairs', 'downstream', 'east', 'far',
#                     'hereabouts', 'indoors', 'inland', 'inside', 'locally', 'near',
#                     'nearby', 'north', 'nowhere', 'outdoors', 'outside', 'overboard',
#                     'overland', 'overseas', 'south', 'underfoot', 'underground',
#                     'underneath', 'uphill', 'upstairs', 'upstream', 'west'}

################################################################################

def enrich_dict(d, category):
    d[category + '_per_description'] = sum(d['num_' + category]) / float(d['num_descriptions'])
    d[category + '_percent'] = (sum(d['num_' + category]) / float(d['num_words'])) * 100
    d[category + '_permille'] = d[category + '_percent'] * 10

################################################################################

def pseudo_quantifier_count(str_description, tokens):
    num_pseudo = word_count(tokens, pseudo_quantifiers)
    for item in pseudo_quantifiers_mwe:
        num_pseudo += str_description.count(item)
    return num_pseudo


def word_count(tokens, words):
    "Helper function to count the number of occurrences of words in tokens."
    overlap = [w for w in tokens if w in words]
    return len(overlap)


def numeral_count(doc):
    "Count the number of numerals in a document."
    numerals = [tok for tok in doc if tok.pos_ == 'NUM']
    return len(numerals)


def linguistic_metrics(descriptions):
    "Function to compute all linguistic metrics."
    descriptions = list(descriptions)
    data = defaultdict(list)
    data['num_descriptions'] = len(descriptions)
    
    # Set up word counter.
    word_counter = Counter()
    
    # Loop over the descriptions and compute different metrics.
    for description in descriptions:
        # Represent the description as a string, so it can be fed to SpaCy.
        str_description = ' '.join(description)
        # Process the description (tokenize, tag, parse).
        doc = nlp(str_description)
        # Count the number of attributive adjectives in the current description.
        # Count numerals as well.
        data['num_attributives'].append(attributive_count(doc))
        data['num_numerals'].append(numeral_count(doc))
        # data['num_nominalizations'].append(num_nominalizations(doc))
        data['num_prepositions'].append(num_prepositions(doc))
        data['num_adverbs'].append(num_adverbs(doc))
        # data['num_predicative'].append(predicative_count(doc))
        
        tokens = [tok.orth_ for tok in doc]
        # And count the number of consciousness of projection terms.
        data['num_consciousness'].append(word_count(tokens, consciousness_of_projection))
        data['num_self_reference'].append(word_count(tokens, self_reference_words))
        data['num_pos_allness'].append(word_count(tokens, positive_allness))
        data['num_negations'].append(word_count(tokens, negations))
        # data['num_pronoun_it'].append(word_count(tokens, pronoun_it))
        # data['num_downtoners'].append(word_count(tokens, downtoners))
        # data['num_amplifiers'].append(word_count(tokens, amplifiers))
        # data['num_place_adverbials'].append(word_count(tokens, place_adverbials))
        
        data['num_pseudo_quantifiers'].append(pseudo_quantifier_count(str_description, tokens))
        # Count the words in the description.
        word_counter.update(tokens)
    
    data['counts'] = word_counter
    data['num_words'] = sum(word_counter.values())
    
    for category in ['adverbs',
                     #'amplifiers',
                     'attributives',
                     'consciousness',
                     #'downtoners',
                     'negations',
                     #'nominalizations',
                     'numerals',
                     #'place_adverbials',
                     'pos_allness',
                     #'predicative',
                     'prepositions',
                     'pseudo_quantifiers',
                     'self_reference']:
        enrich_dict(data, category)
    return data
