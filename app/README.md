 One-Click Data Visualization Application

**Hello researchers and datascientists alike!** Lemur's OCDVA is a web-application allowing you to investigate multimodal datasets and **look at your data** before you hop into next level analyses.

### Running the Application

Web service that utilizes Lemur to generate visualizations for its users.

Clone our git repository:

`git clone https://github.com/NeuroDataDesign/lemur.git`

Add your AWS Credentials to the app/dir directory:

`cp path/to/your/credentials ./app/credentials/credentials`

Make sure your credentials are saved in the format used as a config file stored in the .aws folder:

``` \[default\]
aws_access_key_id = XXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXX
region = XXXXXXXXX```

Go to our app folder:

`cd app`
`docker-compose up`

