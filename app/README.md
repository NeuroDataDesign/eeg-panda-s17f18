 # Lemur's Automatic Visualization Application (LAVA)

**Hello researchers and datascientists alike!** Welcome to LAVA, a web-application that allows you to investigate multimodal datasets and **look at your data** before you move into deeper analyses.

### What is LAVA?

Our mission with LAVA is to provide a breadth of data visualizations with some level of depth to figure out how to gear more in-depth analyses.

### Installing and Running the Application

LAVA requires installation of both [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/).

Clone our git repository:

`git clone https://github.com/NeuroDataDesign/lemur.git`

Add your AWS Credentials to the app/dir directory:

`cp path/to/your/credentials ./app/credentials/credentials`

Make sure your credentials are saved in the format used as a configuration file stored in the .aws folder:

``` \[default\]
aws_access_key_id = XXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXX
region = XXXXXXXXX
```
Go to our app folder:

`cd app`
`docker-compose up`

### Structuring Data
