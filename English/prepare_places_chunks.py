def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

descriptions = list()
with open('./Resources/Places/metadata/utt2ASR') as f:
    for line in f:
        imgid, *tokens = line.split()
        description = ' '.join(tokens) + '\n'
        descriptions.append(description)

gen = chunks(descriptions, 1000)
for i in range(100):
    lines = next(gen)
    with open('./Resources/Places/chunks/places_chunk.{0:03}'.format(i), 'w') as f:
        f.writelines(lines)
