# MRI Analysis Overview and Resources
### Ronak Mehta, September 18, 2017

## What is MRI/fMRI?

Magnetic resonance imaging uses a magnetic field and 
radio waves to capture temporal and spatial images of the brain. 
There is structural MRI (a snapshot of anatomical structure) and 
functional MRI (time series data of blood blow / metabolic processes).

## Difference between structural and functional MRI
| MRI | fMRI |
| --- | --- |
| Focused on anatomical structure | Focused on metabolic processes |
| Shows processes as they happen in space | Shows processes as they happen in time |
| Widely used | Used sparingly |

[[R]](https://theydiffer.com/difference-between-mri-and-fmri/)

## Basic Points

- Two main forms of analysis: whole-brain analysis in which we are looking for the response region of a 
certain cognitive, sensory, or motor process, or region-of-interest (ROI) analysis, where we further 
characterize a specific part of the brain, based on its response to experimental conditions. 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/Preprocessing/BasicfMRIDataAnalysis.html)
- In both cases, there are many preprocessing steps that need to take place. 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/Preprocessing/BasicfMRIDataAnalysis.html)
- When selected a model for “neural activation” used to assess brain activity, it must be 
some function of the blood-oxygen level dependent (BOLD) responses recorded by fMRI. 
[[R]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2587365/)

## Data Structure

- 3D time series (4D total) of voxel shapes, processes other spatial parameters. 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/Preprocessing/BasicfMRIDataAnalysis.html)
- 1D time series of a signal for a particular voxel. As many time series as there are voxels. 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/Preprocessing/BasicfMRIDataAnalysis.html)

## Common Preprocessing Steps 

- Motion Correction / Realignment
- Smoothing 
- Spatial Normalization (to MNI template)

[[R]](http://blogs.discovermagazine.com/neuroskeptic/2010/08/19/fmri-analysis-in-1000-words/#.Wb9ZUMiGPid)

## Statistical/Computational Methods of Interest

- General Linear Model (GLM) on time series. (most common) 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/Preprocessing/BasicfMRIDataAnalysis.html) 
[[R]](http://blogs.discovermagazine.com/neuroskeptic/2010/08/19/fmri-analysis-in-1000-words/#.Wb9ZUMiGPid)
- Independent component analysis (ICA) if main sources of neural activity when given a certain cognitive, sensory, or motor task. 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/Preprocessing/BasicfMRIDataAnalysis.html)
- Multi-Voxel Pattern Analysis (MVPA) - joint-probabilistic analysis of voxel signals in a region, 
to classify that region in particular mental states. 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/MVPA/MultiVoxelPatternAnalysisMVPA.html)  
- Joint analysis in a group study of fMRI scans. Methods outlined in the linked paper:
[[R]](https://www.nature.com/neuro/journal/v20/n3/pdf/nn.4499.pdf)
  - Real-time fMRI analysis (online learning).
  - Multivariate analysis (see MVPA above).
  - Shared-response modelling - map multiple subjects' data to a low dimensional space to capture variation of entire sample.
  - Spatial priors (collected from previous neurological research).
  - Topological Factor Analysis (Similar to ICA but with spatial factors as sources).
  - Covariance between voxels as predictors.
  - Deep Learning (Success with modelling visual system responses).

## Other Resources

- Detailed information about statistical methods and preprocessing steps to take with fMRI data. 
[[R]](http://www.brainvoyager.com/bvqx/doc/UsersGuide/Preprocessing/BasicfMRIDataAnalysis.html)
- Design of fMRI based experiments 
[[R]](http://www.stat.columbia.edu/~martin/Papers/STS282.pdf)
