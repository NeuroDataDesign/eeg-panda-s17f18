# An Multivariate Distance-Based Analytic Framework for Connectome-Wide Association Studies

- Connectome-wide analysis is computationally difficult due to number of comparisons
- Advantages of framework:
    - Don't need to know number of dimensions
    - Don't need to lower resolution
    - No seed selection necessary
    - Don't need to set any parameters
- 4 community based datasets
- Connectome-Wide Association Studies Performed in R, available [here](http://connectir.projects.nitrc.org)
1. Assess subject-level functional connectivity using temporal Pearson correlations
    - Restricted to grey matter voxels present in all subjects
2. Calculate distances between connectivity patterns voxel by voxel for individuals and made distance matrices
3. Use MDMR (multivariate distance matrix regression) to see if phenotypic variable distances correlate with calculated distance matrices
    - Yields pseudo-F statistic
**Resulted in map of brain regions with whole brain pattern connectivity associated with different phenotypic traits**

### Pseudo-F Statistic

- **Goes more in depth than DSM-V**
- Ratio of explained variance and unexplained variance
- Pseudo-F generalizes classical F from Euclidean to any distance

### Significance to Us

- Defined parameter-less analysis algo robustly tested on many results
- Already shown as extendable with the clustering in the phenotypic paper
- Can be extended by using more metrics from fFMRI (partial correlation, directional info, etc)
