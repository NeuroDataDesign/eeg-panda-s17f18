#!/bin/bash

# A script to transform a HBNB csv
# to the PANDA format described
# https://github.com/NeuroDataDesign/orange-panda-f16s17/blob/master/notes/pipeline/data_format.md
#
# Usage: code/scripts/HBNB_to_PANDA.sh -i data/path-to-raw-data-csv -o data/path-to-new-file/file.pkl


while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -i|--input)
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

echo "Converting $INPUT to $OUTPUT"

python lemur/scripts/HBNB_to_PANDA.py $INPUT $OUTPUT
