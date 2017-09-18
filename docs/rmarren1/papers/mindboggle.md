# Mindboggling morphometry of human brains
Klein, Ghosh, Bao
### Notes
* Mindboggle can be used to take in preprocessed T1-weihted MRI data and outputs
  volume, surface, and tabular data
* Useful for study of shape variation in healthy and diseased patients
* Brain image morphometry can be used as a biomarker for diagnosing,
  tracking, and predicting mental health disorders
* Computes many shapes:
  * area
  * volume
  * thickness
  * curvature
  * depth
  * laplace-beltrami spectra
  * zernike moments
  * ect.
* software available on github
* automates extraction, identification, and analysis of MRI data
  * gray/white matter segmentation
  * new algorithms for colume and shape measurements
  * new shape based feature extraction algorithm
* promising experimental results for use of biomarkers in mental health prediction
  * citations 1 through 12
  * mainly held back by the variation that exists in the human brain from subject to subject
  * we must first figure out the normal range of variation to tell who is the outlier
    ( and thus may have something different about their brain causing illness )
* comparing brains is difficult
  * ubiquitously done by co-registering images to the same atlas or reference image
    * imperfect and has some problems (13 - 15)
  * many brain imaging studies ignore this and assume alignment of anatomy, even when
    comparing volumetrically small regions
* volume and thickness measurements are useful in many diagnoses
  * citations 30 - 46
* from scratch in python with some C++ mesh calculations
* mindboggle 101 - 101 manually labeled cortical images
* ROYGBIV - project for online interactive viewing of shape analysis data
* Released as a docker container!
* Processing doesnt take too long (100 mins on macbook pro)
* full documentation available at http://mingboggle.info/software.html
* Is a BIDS-app!
* circle-ci


### Different ways of comparing image shape
* compare grayscale values within a volume
  * does not work well for features of a limited extent
* coregister brains with a reference and calculate shape based on the reference
* directly measure geometric properties (which are invariant to scale, location, rotation)

### Variation in brain shape
* Use a notion similar to discriminibility to test for meaningfulness of the returned measures
  * consistency of shape measures between MRI scans of the same person
  * should be more sensitive to differences in anatomy than differences in MRI scanner setup or
    artifacts
* Study done on the mindboggle 101 dataset to get a sense for the normal
  geometric variation in brain shape

### Use for our project?
* good pipeline to give us shape based biomarkers for mental illness
* good visualization tool already available, don't have to re-do
* offers a good model for a feature extraction pipeline, maybe
  something similar can be done with eeg?
* already ported many analysis algorithms to python, we can use these!

