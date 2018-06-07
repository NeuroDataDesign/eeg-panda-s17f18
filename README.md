# lemur-s17f18

Welcome to the Lemur Repository! 

Be sure to check out our [main website](https://neurodatadesign.github.io/lemur/) or [final presentation slides](https://docs.google.com/presentation/d/1aU0Sz5DRoYPoJU6ENPEkCqxzHaQcjo4hAYj5pnbdNNM/edit?usp=sharing).

Here is some of the founding work for our project:
- [Motivating Research](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/Literature%20Scoping.pdf)
- [Proposal Slides](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/proposal.pdf)
- [Statement of Work](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/sow.md)

Explore some of our different projects:

- [LEMUR Coding Package](https://github.com/NeuroDataDesign/lemur/tree/master/lemur): LEMUR is a tool that can assist in the aggregate and one-to-one visualization of any set of data points. While this project was designed to assist in the visualization of multi-modal neuroscience/psychology datasets, it can be used for any set of objects and similarity / dissimilarity function acting on pairs of such objects.
    - [Demo Notebook](http://nbviewer.jupyter.org/github/NeuroDataDesign/lemur/blob/master/docs/notebooks/rmarren1/Lemur%20fMRI.ipynb)
    - [AWS Grant Application](https://github.com/NeuroDataDesign/lemur-f17s18/blob/master/docs/group/proposal/Multi-Modal%20Brain%20Visualizations.pdf)
- [LAVA (One-Click Web Application)](https://github.com/NeuroDataDesign/lemur/tree/master/app): LAVA is a **one-click** web-application that allows you to investigate multimodal datasets and **look at your data** before you move into deeper analyses.
- [Run Everything (P-Factor Exploration)](https://github.com/NeuroDataDesign/lemur/tree/master/docs/notebooks/vidurkailash/run_everything): The HBN (Healthy Brain Network) provides a rich and robust dataset that collects multiple different modalities of neurological data (EEG and multiple modalities of MRI) for subjects with a variety of phenotypes. With the data it provides, we wanted to explore different levels of correlation/similarities we could find between neuroimaging data and the p factor a metric that can be created from the results of different phenotypic tests. We preprocessed our data using PANDA (EEG) and ndmg (MRI). We calculated this similarity using MGC, an algorithm that categorizes not only global correlation but similarities in local regions.

**What is below this point we have left as documentation of previous work on the site, but is currently outdated.**

***

### Sprint 2 Demo

[Docker documentation and demo can be found at our dockerhub.](https://hub.docker.com/r/nkumarcc/redlemur/)

### Sprint 1 Release:
[Sprint 1 Demo Slides](https://docs.google.com/presentation/d/1WhvT_KDLle6KnK6QdVPW1PvJf-FzisBHaIJUEnq5vf0/edit?usp=sharing)

* Research


##### Download
* [PyPI release](https://pypi.python.org/pypi/redlemur)
* `pip3 install redlemur` and then `import lemur`

![](https://user-images.githubusercontent.com/10272301/32417867-a9e85e72-c22d-11e7-9f56-9f1dd2b062c0.png)
Multi-Modal Neuroimaging visualizaitons made easy!
