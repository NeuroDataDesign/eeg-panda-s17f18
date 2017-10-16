#!/bin/bash

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -i|--in)
    INPUT="$2"
    shift # past argument
    ;;
    -o|--out)
    OUTPUT="$2"
    shift # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done


for D in $INPUT/*/;
do
    DIRNAME=$(basename $D)
    INDIR=$INPUT/$DIRNAME/EEG/raw/csv_format/$DIRNAME_RestingState_data.csv
    OUTDIR=$OUTPUT/$DIRNAME/resting/eeg
    mkdir -p $OUTPUT/$DIRNAME/resting/eeg
    ./code/scripts/HBNB_to_PANDA.sh -i done
