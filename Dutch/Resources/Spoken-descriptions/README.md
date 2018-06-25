# Reproduction steps

This folder contains files to preprocess the DIDEC data (given in DIDEC-plain).
You don't need to do this, because the files are already preprocessed.

## Requirements

* Python 3.6
* Frog 0.14 (based on ucto 0.12, libfolia 1.12, timbl 6.4.10, ticcutils 0.18, mbt 3.3.1)

We installed `frog` using `homebrew` on macOS, using [this GitHub](https://github.com/fbkarsdorp/homebrew-lamachine).
Instructions for installation:

```
brew tap fbkarsdorp/homebrew-lamachine
brew install ucto
brew install frog
```

If you're not a Mac user, see the instructions [here](https://proycon.github.io/LaMachine/).

## How to use the scripts in this folder

1. Run `bash frog.sh`
2. Run `python fix_preprocessing.py`
