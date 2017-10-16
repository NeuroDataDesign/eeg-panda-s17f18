#!/bin/bash

# Script to download subset of subjects from the fcp-indi s3 bucket
# ./HBNB_to_PANDA.sh -i data/NDARAA075AMK/EEG/raw/csv_format/NDARAA075AMK_Video1_data.csv -o data/NDARAA075AMK/EEG/raw/PANDA/NDARAA075AMK_Video1_data.pkl

SUBJECTS=("NDARAD481FXF" "NDARAE199TDD" "NDARAJ366ZFA" "NDARAK187ZLP" "NDARAM277WZT" "NDARAT100AEQ" "NDARAT299YRR" "NDARAV894XWD")

for subject in ${SUBJECTS[@]}
do
    ./HBNB_download.sh -sub $subject -o ../../data
done

