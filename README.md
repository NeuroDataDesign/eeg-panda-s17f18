# lemur-s17f18

Welcome to Lemur!

Lemur is a library to assist in the aggregate and one-to-one visualization of any set of data points. This tool was designed to assist in the visualization of multi-modal neuroscience/psychology datasets, but it can be used for any set of objects and similarity / dissimilarity function acting on pairs of such objects.

### Sprint 2 Demo

##### 1. Download the Demo Files
* Go to https://drive.google.com/open?id=163zn9TwyKqs6yPtJ9DsilGibk8S1E4ji
  * Download the file using the download button in the upper right hand side of the page.
* Go to https://drive.google.com/open?id=1r_EAtJUK7NA-tbzCdi5_8rxIHHIEI5nn
  * Download the file using the downloadbutton in the upper right hand side of the page.

##### 2. Pull the Docker Image
* Pull the docker image with `docker pull rymarr/lemur`

##### 3. Launch the Docker Image
* Launch the docker image with `docker run -p 5000:5000 rymarr/lemur`

##### 4. Launch a New Image Processing Job
* Go to the 'Upload' tab
![](https://user-images.githubusercontent.com/10272301/34256327-cafa91ca-e622-11e7-90be-1f4c228bc996.png)

* Click on the button to upload a phenotypic .csv file
![](https://user-images.githubusercontent.com/10272301/34256328-cb0ad42c-e622-11e7-93b3-709f772c9fb0.png)

* Navigate to the iris.csv file and choose it
![](https://user-images.githubusercontent.com/10272301/34256329-cb183342-e622-11e7-9fd6-68ceeea0b4d3.png)

* Click on the button to upload a EEG credentials .csv file
![](https://user-images.githubusercontent.com/10272301/34256330-cb2663ae-e622-11e7-99a6-831caf415219.png)

* Navigate to the test.csv file and choose it
![](https://user-images.githubusercontent.com/10272301/34256331-cb359766-e622-11e7-8481-85b32563a26f.png)

* Click on the button to upload a fMRI credentials .csv file
![](https://user-images.githubusercontent.com/10272301/34256332-cb438fc4-e622-11e7-88fd-6a878d973cb5.png)

* Navigate to the test.csv file and choose it
![](https://user-images.githubusercontent.com/10272301/34256333-cb511a68-e622-11e7-97a1-51c80faf7e4d.png)

* Name your new dataset `test`
![](https://user-images.githubusercontent.com/10272301/34256334-cb60425e-e622-11e7-8a5e-daa2fefa0dd5.png)

* Click the upload button, and wait without touching anything. You can check the progress of the job by opening the terminal from which the docker image was launched from.

* You will automatically be redirected to the EEG plots page when this process is complete.

##### 5. Navigating to Different Modalities
* To get to another modality other than EEG (remember, this is where you were automatically directed), click the home button in the upper menu bar.

* You will see three sections for Phenotypic, EEG, and fMRI data respectively. Clicking the blue link with the name of your dataset will redirect you to the page with the plots for that modality.


### Sprint 1 Release:
[Sprint 1 Demo Slides](https://docs.google.com/presentation/d/1WhvT_KDLle6KnK6QdVPW1PvJf-FzisBHaIJUEnq5vf0/edit?usp=sharing)

##### Demos
* [EEG Demo](https://nbviewer.jupyter.org/github/NeuroDataDesign/lemur-f17s18/blob/master/docs/notebooks/rmarren1/Lemur%20EEG.ipynb)
* [fMRI Demo](https://nbviewer.jupyter.org/github/NeuroDataDesign/lemur-f17s18/blob/master/docs/notebooks/rmarren1/Lemur%20fMRI.ipynb)
* [Phenotypic Demo (images not live due to data usage agreement)](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/notebooks/rmarren1/Lemur%20Phenotypic.ipynb)

##### Documentation
* Code
  * [lemur Package Documentation](https://neurodatadesign.github.io/lemur-f17s18/)
  * [AWS Grant Application](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/Multi-Modal%20Brain%20Visualizations.pdf)
* Research
  * [Motivating Research](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/Literature%20Scoping.pdf)
  * [Proposal Slides](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/proposal.pdf)
  * [Statement of Work](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/sow.md)

##### Download
* [PyPI release](https://pypi.python.org/pypi/redlemur)
* `pip3 install redlemur` and then `import lemur`

![](https://user-images.githubusercontent.com/10272301/32417867-a9e85e72-c22d-11e7-9f56-9f1dd2b062c0.png)
Multi-Modal Neuroimaging visualizaitons made easy!
