# Instructions to reproduce our results

## Requirements

* CPIDR 3.2.3738.41169
* Python 3.6
    - tabulate 0.7.7
    - spacy 2.0.4
    - pyphen 0.9.4
    - matplotlib
    - numpy 1.13.1
    - seaborn 0.7.1

## Steps

* First unzip the MS COCO data in `Spoken-versus-Written/English/Resources/MSCOCO`.

### Main table

Please run the following commands in order:

* `bash run_analysis.sh`
* `python generate_table.py`

You should now have the same table as in our paper.

### Propositional Idea Density

To compute the propositional idea density (PID) scores, you need to use the CPIDR
tool. We ran this tool through Wine. First, preprocess the image descriptions:

* `python prepare_coco_train_chunks.py`
* `python prepare_flickr_train_chunks.py`
* `python prepare_places_chunks.py`

Then, you will have a folder full of files with exactly 1000 descriptions each in
`./Resources/<Dataset>/`. Analyze these files with the CPIDR tool. We stored the
output of this analysis in `./Results/`. Because CPIDR cannot handle many files at once,
we had to analyze the files for the Places corpus in two stages. Therefore the `Results/`
folder contains three files for the Places data (for full transparency):

* `./Results/Places-00-47-CPIDR-results.txt`
* `./Results/Places-48-99-CPIDR-results.txt`
* `./Results/Places-merged-CPIDR-results.txt`

To finish the PID-analysis, run:

* `python plot_densities.py`
