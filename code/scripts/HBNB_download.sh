#!/bin/bash

# A script to transform a direct download from
# http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/downloads_EEG.html
# to the PANDA format described
# https://github.com/NeuroDataDesign/orange-panda-f16s17/blob/master/notes/pipeline/data_format.md

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
