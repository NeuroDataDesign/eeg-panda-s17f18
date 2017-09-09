#!/bin/bash

# Script to download a subject file from the fcp-indi s3 bucket
#
# Usage: code/scripts/HBNB_download.sh -sub subject-id -o data
#

export BUCKET="fcp-indi"
export BASE_PATH="/data/Projects/HBN/S1/EEG/"

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -sub|--subject-id)
    SUBJECT="$2"
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


export FILE_NAME=$SUBJECT".tar.gz"
export REMOTE_PATH="s3://"$BUCKET$BASE_PATH$FILE_NAME
export LOCAL_PATH=$OUTPUT"/"$FILE_NAME

echo "Pulling data from $REMOTE_PATH"
echo "Pushing data to $LOCAL_PATH"

aws s3 cp $REMOTE_PATH $LOCAL_PATH
tar -zxf $LOCAL_PATH -C $OUTPUT
rm $LOCAL_PATH
