# lemur-s17f18

Welcome to Lemur!

Lemur is a library to assist in the aggregate and one-to-one visualization of any set of data points. This tool was designed to assist in the visualization of multi-modal neuroscience/psychology datasets, but it can be used for any set of objects and similarity / dissimilarity function acting on pairs of such objects.

### Sprint 2 Demo

* run in a terminal `docker pull yujialiu/redlemur:latest`
* run in a terminal `docker run -p 127.0.0.1:5000:5000 -t yujialiu/redlemur:latest`
* go to `localhost:5000`
* download the iris.csv file from the base directory of lemur, which can be done with `wget https://raw.githubusercontent.com/NeuroDataDesign/lemur/master/iris.csv`
* under 'Pipeline Upload' click 'choose file' then direct to the `iris.csv` file
* Click 'Upload'
* Wait about 15 seconds
* Click on plots in the left menu bar to display them in the center.


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
