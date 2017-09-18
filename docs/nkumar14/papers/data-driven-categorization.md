# Data-Driven Phenotypic Categorization for Neurobiological Analyses: Beyond DSM-5 Labels

### Main Ideas

- Weaknesses of categorical definitions of illnesses are increasingly apparent
- Labels are necessary for clinical practice but impede search for pathophysiological biomarkers
- Attempting to create new nosology, but unclear how best to define categories
- Data-driven approaches may help identify more behaviorally refined biological phenotypes to address the profound heterogeneity
- **Process**
    - Get dataset
    - Identify data-driven phenotypes based on core behavioral features
    - First aim was to identify phenotypic dimensions that accurately represent meaningful variation across multiple domains of behavior
        - Bootstrap-based (?) exploratory factor analysis on 49 subscales derived from 10 measures obtained for 347 participants
    - Second aim Identify nested hierarchy of homogenous patient groups via hybrid hierarchical clustering (HHC)
    - Third aim examine multivariate intrinsic brain functional connectivity differences among adjacent clusters and groups

### Methods & Materials

- Particiapts
    - Nathan Kline Institute-Rockland Sample (NKI-RS)
        - 1000 participants
        - 8 - 85 years
    - Inclusion criteria:
        1. 18 - 59 years of age
        2. Absence of head injury or major neruo disorder
        3. Negative history of bipolar disorder or psychosis
        4. Negative drug test for common drugs with no therapeutic reasons
        5. At least 95% completion of each self-report measure
- Subject Phenotyping
    - Completed Structured Clinical Interview:
        - DSM-IV Axis I Disorders (SCID)
        - Edinburgh Handedness Inventory
        - Other measures of clincial symptoms and broad behavioral characterisitcs
    - Used subscales of phenotyping
- MRI Acquisition
    - 3T Siemens TIM Trio system
    - 32 channel head coil
    - Structural Image
        - T1-weighted magnetization prepared gradient echo sequence
        - Repetition Time = 1900ms
        - Echo Time = 2.52ms
        - Flip Angle = 9 deg
        - 176 Slices, 1 mm^3 isotropic voxels
    - Resonance Imaging
        - Multiband echo-planar imaging
        - Volumes = 900
        - Repetition Time = 645ms
        - Echo Time = 30 ms
        - Flip Angle = 60 deg
        - 3 mm^3 isotropic voxels
- **Phenotypic Analysis**
    - **Data Screening**
        - All self-report data was checked for outliers
        - Missing data calculated with EM algo
    - **Dimension Reduction (done on each participant)**
        1. Multidim Phenotypic Profile using 49 subscale scores obtained from 10 questionnaires
        2. Exploratory Factor Analysis (EFA) to obtain reduced dimensions
        3. Age and gender regressed residuals of the 49 scores to minimze demographic influence
        4. Parrallel analysis of 10,000 permutations of the raw data was used to determine number of factors
        5. Max Likelihood Factor estimation with varimax rotation was used to estimate 6 factor loadings for each subscale score
        6. Confidence intervals for factor loadings were estimated from 10,000 bootstrapped resamplings
        7. Factor loadings overlapping 0 or exhibiting values less than |0.25| were set to 0 in restricted model
    - **Clustering Analysis**
        - HHC using tree-structured vector quantization to identify nested participant groups based on Euclidean distances between participant factor score profiles
            - Identifies mutual clusters (close to one another but far from others), constrained divisive clustering (retaining mutual clusters), and divisive clustering (division of mutual clusters)
    - **Cluster Comparisons**
        - Pairwise comparisons were made among adjacent clusters at each level using EFA, ASR, and SCID
        - Used cut scores on ASR to achieve meaningful groupings
- MRI Processing
    - Preprocessing- [read the paper, search R-fMRL Preprocessing](http://www.sciencedirect.com/science/article/pii/S0006322316325860?via%3Dihub)
    - Multivariate Distance Matrix Regression
        - Compared functional connectivity profiles of different adjacent levels of hierarchy 
        - Voxel by voxel, 3 steps:
            1. Pearson's correlation between voxel and the rest of the voxels in same brain
            2. Distance matrix reflecting distance between maps from both subjects from step 1
                - Distance defined as sqrt(2 * (1 - r)) where r is spatial correlation
            3. Pseudo-F statistic computed to evaluate relationship between distance matrix and variable of interest (cluster membership)
        
### Results

- **Dimension Reduction**
    - Parallel analysis -> 6 factor solution accounting for 77.8% of the variance
    - Constrained model (eliminated low-loading items) accounted for 65.4% of variance
    - 6 Factors:
        1. General distress and impairment
        2. Conscientiousness
        3. Sensation and risk seeking
        4. Frustration intolerance
        5. Contextual sensitivity
        6. Neuroticism and negative affect
- **Cluster Analysis**
    - 3 clear cutpoints from dendrogram yielding 8 groups
    - Largest ***CHC (Calinski-Harabasz criterion)*** value was observed at *k* = 2 and stable subgroups at *k*  = 4 and 8
- **Phenotypic Cluster Differences**
    - 3 levels of dendrogram
    - **Level 1:**
        - Robust, reflecting broad-reaching group differences
        - C1: adaptive functionality, C2; maladaptive functionality
    - **Level 2:**
        - C2 divided into internalizing and externalizing charactersistics
        - C2a: higher rates of lifetime psych diagnosis, C2b: higher senstaion and risk seeking (external)
    - **Level 3:**
        - Divided into 8 subclusters, much fewer significant pairwise differences between subclusters (other than C2a2 had  more psychopathology than C2a1)
- Multivariate Intrinsic Connectivity Differences Among Clusters
    - Only MDMR on first level of clusters survived comparison corrections
    - 3 clusters found
    - Cluster 1: Bilateral primary and secondary somatosensory cortices as well as premotor, motor, and supplementary motor regions and approximately centered on midline near supplementary motor area
    - Cluster 2: Centered on left thalamus, limbic regions, decision-making regions
    - Cluster 3: Right hippocampus

### Discussion

- Found personality traits like conscientiousness can be used to differentiating groups
- Somamotor network which was the largest distinguishing functional cluster is a novel target for usage in diagnoses

## Significance to Us

- Number of fMRI and phenotypic methods that we can use
- Clustering methods across different dimensions and combining with fMRI data
- Shown results from such measures on another large dataset
