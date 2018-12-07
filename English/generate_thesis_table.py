import json
from tabulate import tabulate

def load_json(filename):
    "Load a JSON file and return its contents."
    with open(filename) as f:
        data = json.load(f)
    return data

################################################################################
# Load data

entries = [("MS COCO", load_json('./Results/coco_results.json')),
           ("Flickr30K", load_json('./Results/flickr_results.json')),
           ("Places", load_json('./Results/places_results.json'))]

################################################################################
# Table 1: general statistics.

rows = []
for name, data in entries:
    # Necessary to cover both the parallel datasets (MS COCO & Flickr30K) and Places.
    try:
        # For the parallel datasets.
        msttr = data['msttr']['parallel']
    except TypeError:
        # For Places.
        msttr = data['msttr']
    # Create row.
    row =  [name,
            "{:,d}".format(data['lengths']['num_descriptions']),
            "{:,d}".format(data['lengths']['num_tokens']),
            "{:,d}".format(len(data['words']['counts'])),
            "{:.2f}".format(msttr)]
    rows.append(row)

table = tabulate(rows,
                 headers = ['Name', 'Descriptions', 'Tokens', 'Types', 'MSTTR'],
                 tablefmt = 'latex_booktabs')
table = table.replace('{llllr}','{lrrrr}')
print(table)
print()

################################################################################
# Table 2: features.

rows = []
for name, data in entries:
    # Make smaller differences visible.
    data['words']['consciousness_permille'] = data['words']['consciousness_percent'] * 10
    data['words']['self_reference_permille'] = data['words']['self_reference_percent'] * 10
    data['words']['attributives_permille'] = data['words']['attributives_percent'] * 10

    row =  [name,
            #"{:,d}".format(data['lengths']['num_descriptions']),
            #"{:,d}".format(data['lengths']['num_tokens']),
            "{:.2f}".format(data['lengths']['avg_token_length_syll']),
            "{:.2f}".format(data['lengths']['avg_token_length_char']),
            "{:.2f}".format(data['lengths']['avg_desc_length_syll']),
            "{:.2f}".format(data['lengths']['avg_desc_length_tok']),
            "{:.2f}".format(data['words']['attributives_per_description']),
            "{:.2f}".format(data['words']['attributives_permille']),
            "{:.2f}".format(data['words']['adverbs_per_description']),
            "{:.2f}".format(data['words']['adverbs_permille']),
            "{:.2f}".format(data['words']['prepositions_per_description']),
            "{:.2f}".format(data['words']['prepositions_permille']),]
    rows.append(row)

table = tabulate(rows,
                 headers = ['Name', 'Syll', 'Char', 'Syll', 'Tok', 'Desc', 'PERM', 'Desc', 'PERM', 'Desc', 'PERM'],
                 tablefmt = 'latex_booktabs')


additional_header = """\\toprule
& \multicolumn{2}{c}{TokLen} &\multicolumn{2}{c}{DescLen} & \multicolumn{2}{c}{Attributives} & \multicolumn{2}{c}{Adverbs} & \multicolumn{2}{c}{Prepositions}\\\\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}\cmidrule(lr){10-11}"""
table = table.replace('\\toprule', additional_header)
table = table.replace('Places','\midrule\nPlaces')
table = table.replace('0    &','0.00 &')
table = table.replace('1.3  &','1.30 &')
table = table.replace('10.5  &','10.50 &')
table = table.replace('12.2  &','12.20 &')
table = table.replace('{lrrrrrrrrrr}','{lcccccccccc}')
table = table.replace('PERM', '\\textperthousand')
print(table)
print('\n\\vspace{5px}\n')
#
# # Space savers:
# #table = table.replace('\\toprule','\cmidrule[\heavyrulewidth](lr){1-13}')
# #table = table.replace('\midrule','\cmidrule(lr){1-13}')
# #table = table.replace('\\bottomrule','\cmidrule[\heavyrulewidth](lr){1-13}')
# print(table)
# print()
# print('Continued:')

###########################
# Part 2 of the table

rows = []
for name, data in entries:
    row = [name,
           # "{:.2f}".format(msttr),
           "{:.2f}".format(data['words']['consciousness_per_description']),
           "{:.2f}".format(data['words']['consciousness_permille']),
           "{:.2f}".format(data['words']['self_reference_per_description']),
           "{:.2f}".format(data['words']['self_reference_permille']),
           "{:.2f}".format(data['words']['pos_allness_per_description']),
           "{:.2f}".format(data['words']['pos_allness_permille']),
           "{:.2f}".format(data['words']['negations_per_description']),
           "{:.2f}".format(data['words']['negations_permille']),
           "{:.2f}".format(data['words']['pseudo_quantifiers_per_description']),
           "{:.2f}".format(data['words']['pseudo_quantifiers_permille'])
           # "{:.2f}".format(data['words']['numerals_per_description']), # Not significant according to DeVito
           # "{:.2f}".format(data['words']['numerals_permille']),        # Not significant according to DeVito
           ]
    rows.append(row)

table = tabulate(rows,
                 headers=['Name', 'Desc', 'PERM', 'Desc', 'PERM', 'Desc', 'PERM', 'Desc', 'PERM', 'Desc', 'PERM'],
                 tablefmt='latex_booktabs')

additional_header = """\\toprule
 & \multicolumn{2}{c}{Consciousness} & \multicolumn{2}{c}{Self-reference} & \multicolumn{2}{c}{Allness} & \multicolumn{2}{c}{Negations} & \multicolumn{2}{c}{PseudoQuant} \\\\
\cmidrule(lr){2-3} \cmidrule(lr){4-5} \cmidrule(lr){6-7} \cmidrule(lr){8-9} \cmidrule(lr){10-11}
"""
table = table.replace('Places','\midrule\nPlaces')
table = table.replace('0    &', '0.00 &')
table = table.replace('1.3  &', '1.30 &')
table = table.replace('{lrrrrrrrrrr}','{lcccccccccc}')
table = table.replace('\\toprule', additional_header)
table = table.replace('PERM', '\\textperthousand')
print(table)
