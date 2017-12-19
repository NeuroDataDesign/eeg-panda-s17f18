#/bin/bash
jupyter nbconvert --to python --output ../../../lemur/scripts/pheno.py docs/notebooks/rmarren1/Pheno-runnable.ipynb
jupyter nbconvert --to python --output ../../../lemur/scripts/fmri.py docs/notebooks/rmarren1/fMRI-runnable.ipynb
jupyter nbconvert --to python --output ../../../lemur/scripts/eeg.py docs/notebooks/rmarren1/EEG-runnable.ipynb
