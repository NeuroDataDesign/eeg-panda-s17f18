### Getting the subject IDS for each data release
* EEG Data
  * Data release one:
    * `aws s3 ls s3://fcp-indi/data/Projects/HBN/R1/EEG/ | awk '{print $4}' | awk -F. '{print $1}'
`
  * Data release two:
    * `aws s3 ls s3://fcp-indi/data/Projects/HBN/R2/EEG/ | awk '{print $4}' | awk -F. '{print $1}'
`
* MRI Data
  * Data release one:
    * `aws s3 ls s3://fcp-indi/data/Projects/HBN/R1/MRI/RU/ | awk '{print $4}' | awk -F. '{print $1}'
`
  * Data release two:
    * `aws s3 ls s3://fcp-indi/data/Projects/HBN/R2/MRI/ | awk '{print $4}' | awk -F. '{print $1}'
`
