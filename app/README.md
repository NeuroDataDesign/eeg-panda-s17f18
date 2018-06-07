 # Lemur's Automatic Visualization Application (LAVA)

**Hello researchers and datascientists alike!** Welcome to LAVA, a web-application that allows you to investigate multimodal datasets and **look at your data** before you move into deeper analyses.

## What is LAVA?

Our mission with LAVA is to provide a breadth of data visualizations with some level of depth to figure out how to gear more in-depth analyses. To do so, we provide visualizations of raw data, data transformed with multi-dimensional scaling, data that has been run through adaptive clustering algorithms (Adaptive KMeans or Hierarchial Gaussian Mixture Models), and one-to-one plots for EEG data.

#### List of Provided Visualizations:

Visit [our website](https://neurodatadesign.github.io/lemur/) to see images representing some of these different plots.

| Raw Data Plots         | Multi Dimensional Scaling Plots        | Clustering Plots              | EEG One-to-One Plots |
| ---------------------- | -------------------------------------- | ----------------------------- | -------------------- |
| Correlation Matrix     | Correlation Matrix                     | Cluster Means Dendogram       | Connected Scatter    |
| Heatmap                | Heatmap                                | Cluster Means Level Heatmap   | Sparkline            |
| Eigenvector Heatmap    | Eigenvector Heatmap                    | Cluster Means Level Lines     | Spatial Periodogram  |
| Histogram Heatmap      | Histogram Heatmap                      | Pairs Plot                    | Spatial Time Series  |
| Location Heatmap       | Location Heatmap                       | Stacked Cluster Means Heatmap |                      |
| Location Lines         | Location Lines                         |                               |                      |
| Scree Plot             | Scree Plot                             |                               |                      |


## Installing and Running the Application

LAVA requires installation of both [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/).

Clone our git repository:

`git clone https://github.com/NeuroDataDesign/lemur.git`

Add your AWS Credentials to the app/dir directory:

`cp path/to/your/credentials ./app/credentials/credentials`

Make sure your credentials are saved in the format used as a configuration file stored in the .aws folder:

```
[default]
aws_access_key_id = XXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXX
region = XXXXXXXXX
```
Go to our app folder:

```
cd app
docker-compose up
```

#### Structuring Data

| Data Modality            | Format of File                        | Upload Method            |
| ------------------------ | ------------------------------------- | ------------------------ |
| Categorical/Phenotypic   | .csv                                  | Directly from computer   |
| EEG                      | .pkl (Python 3 pkl), location of channels .csv (format below) | S3 Bucket in BIDS Format |
| fMRI                     | .nii.gz (NIFTI Image)                 | S3 Bucket in BIDS Format |
| Graph Based/Connectomes  | .edgelist (NetworkX Python Package)   | S3 Bucket in BIDS Format |

- **For S3 Buckets**: Amazon Web Services (AWS) is a collection of enterprise-level cloud-based services - among them is the Simple Storage Service (S3), meant to hold large data files in containers called “buckets”. These containers hold massive amounts of data, but the hardware component is abstracted away from the user, so they just can access their files in the cloud. If you want more information, check out https://aws.amazon.com/s3/
    - **Meaning of "Bucket Name" and "Path"**: The bucket name is the name of the S3 bucket you wish to run. The path is the path to whichever directory within the bucket contains all of the BIDS formatted data (eg within your bucket you may store your data in data/bids as opposed to the root folder).
    - **REMEMBER**: Only use public buckets, buckets you own, or buckets the credentials you upload have access to.
- **For BIDS Formatting**: LAVA was made to handle single-session BIDS formatted data. Please look at [the BIDS standard here](http://bids.neuroimaging.io/).
- **For Graph Data**: [NetworkX Python Package](https://networkx.github.io/documentation/networkx-1.9.1/overview.html)
- **For EEG Data**: The channel locations csv ***must be named chanlocs.csv*** and:
    - A header
    - A column of electrode names/numbers
    - 3 subsequent columns with the relative X, Y, and Z locations of the electrodes
    - Example chanlocs.csv format :

         - | labels | X        | Y        | Z        |
           | ------ | -------- | -------- | -------- |
           | E1     | -5.7876  | 5.5208   | -2.5774  |
           | E2     | -5.2918  | 6.7091   | 0.3074   |
           | E3     | -3.8641  | 7.6342   | 3.0677   |
           | ...    | ...      | ...      | ...      |
           
#### Example Data

- Example phenotypic data can be found [here](https://drive.google.com/file/d/163zn9TwyKqs6yPtJ9DsilGibk8S1E4ji/view)
- Example EEG and fMRI buckets (they are entirely public):
    - EEG:
        - Bucket Name: red-lemur-sample
        - Path: eeg
    - fMRI:
        - Bucket Name: red-lemur-fmri-sample
        - Path: fmri
