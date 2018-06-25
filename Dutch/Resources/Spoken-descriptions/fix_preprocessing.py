import glob

def select_lines(filename):
    """
    Select all sentences that are not just a single period.
    This corrects sloppy preprocessing.
    """
    with open(filename) as f:
        lines = []
        skip = False
        for line in f:
            if line.startswith('1\t.'):
                skip = True
                continue
            elif skip:
                skip = False
                pass
            else:
                lines.append(line)
        return lines

files = glob.glob('./DIDEC-tagged/output*.txt')

for filename in files:
    lines = select_lines(filename)
    with open(filename,'w') as f:
        f.writelines(lines)
