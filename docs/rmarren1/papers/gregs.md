# Greg's GREMLIN paper
Greg
### MRI Background
##### General
* Some mental illnesses can be described as connectopathies
  -- illnesses which could appear when studying the connectome,
  a structural map of the brain
* Tools exist to analyze MR images, but are hard to use
* No one click open source cloud parallelizable pipelines (Gregs is)
* Data collection procedures are non-standard
  * Lack of reproducibility
  * Many people overfit tuning parameters to a particular dataset
##### Connectome
* A comprehensive structural description of the network of elements and connections forming the brain
  * Many different kinds based on scale and resolution of data
  * MRI is a macroscale connectome, and good resolution for a non invasive procedure
##### MRI Background
* Brain consists of white matter and gray matter
  * Gray matter is dense in cell bodies, represents processing tissue
  * White matter is dense in connective tissue, represents communication channels
  * These two types exhibit different properties which can be detected by MRI
* Many kinds of MRI that can exploit contrast in brain to take an image
  * functional MRI (fMRI)
    * measures high amounts of blood flow (BOLD)
    * measures masses of cars on the road
  * structural T1 MRI (MPRAGE)
    * based on longitudinal relaxation of tissue, highest clarity image
    * 4 dimensional (x by y by z by D) D is number diffusion directions
    * consist primarily of white matter pathways
    * measures cities
  * diffusion weighted MRI (DWI)
    * diffusion tensor imaging (DTI)
    * diffusion spectral imaging (DSI)
    * high angular resolution diffusion imaging (HARDI)
    * measures highways
##### ndmg
* one click brain images -> graphs pipeline
  * neurodata's mri graph pipeline
* requires subject specific data and template specific data
  * atlases -- reference image of standard brain parcellation
* preprocessing
  * ensure b vectors and b values are in proper format
* registration
  * puts data from different humans on a common coordinate system for comparison
  * use the MNI152 atlas
  * to prevent introduction of data from transforming data, series of alignments introduced
    * individual alignment - DTI is D-length sequence of 3d images
    * subject may have shifted slightly during sequential process of taking all of these
  * Eddy currents - circular loops of currents induced on surface of tissue when
    subject introduced to magnetic field
    * Use FSL's eddy current correction module
  * Using FSL's FLIRT linear registration, align B0 volume to MPRAGE scan, and
    MPRAGE to template volume
  * combine the transforms used and apply to rest of image stack
  * resample to align image space to voxel space
* tractography
  * first step tensor estimation
    * turn 4 dimensional DTI volume into 3 dimensional tensor image
    * each voxel defined by a tensor rather than an intensity
    * tensor represented by three eigen vectors, one in each principal coordinate frame axis
    * if intensity along each axis equal, tensor is a sphere
    * DiPY diffusion processing package
  * fractional anisotropy
    * ratio of largest eigen value to sum of all eigen value
    * measure of strength of flow
  * then tractography using DiPY EuDX
    * deterministic
* graph creation
  * creating graph images from fibers/streamlines using Networkx
  * add metadata, save to database

