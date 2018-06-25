# Installed
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import numpy as np

# Stdlib
import csv


sns.set_style("whitegrid")
sns.set_context('paper', font_scale=2)
my_palette = sns.color_palette("cubehelix", 3)
sns.set_palette(my_palette)


def get_entries(filename):
    "Get data from a TSV file, after skipping the first line."
    with open(filename) as f:
        # Skip the first line, which contains the CPIDR version.
        next(f)
        reader = csv.DictReader(f,delimiter='\t')
        return list(reader)


def get_densities(entries):
    "Get the density values, remove spaces, and convert to floats. Return array."
    density_list = [float(entry['Density'].strip()) for entry in entries]
    return np.array(density_list)


def load_densities(filename):
    "Load densities from a CPIDR 3 file. Prints number of values, returns array."
    entries = get_entries(filename)
    densities = get_densities(entries)
    print(len(densities),'values loaded.')
    return densities


coco = load_densities('./Results/COCO-CPIDR-results.txt')
flickr = load_densities('./Results/Flickr-CPIDR-results.txt')
places = load_densities('./Results/Places-merged-CPIDR-results.txt')

# Create figure
fig, ax = plt.subplots(1,1)

# Plot probability density functions

sns.rugplot(coco, alpha=0.75, color=my_palette[0], height=0.04)
sns.rugplot(flickr, alpha=0.75, color=my_palette[1], height=0.04)
sns.rugplot(places, alpha=0.75, color=my_palette[2], height=0.04)

sns.kdeplot(coco, shade=True, alpha=0.75, label="MS COCO")
sns.kdeplot(flickr, shade=True, alpha=0.75, label="Flickr30K")
sns.kdeplot(places, shade=True, alpha=0.75, label="Places")
sns.despine()

# Create legend markers
legend_markers = [Line2D(range(1), range(1),
                         color="white",
                         linewidth=0,
                         marker='o',
                         markersize=15,
                         markerfacecolor=my_palette[i]) for i in range(3)]

# Add legend
leg = plt.legend(legend_markers,('MS COCO','Flickr30K', 'Places'), numpoints=1, loc=1, handletextpad=-0.3)

# Modify labels. (For some reason I got numbers > 1, which doesn't match the probability.)
ax.set_yticklabels([None] + [i/10 for i in range(6)])

plt.xlabel("Propositional Idea Density")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('./Results/PID-plot.pdf')
