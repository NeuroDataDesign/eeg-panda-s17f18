# Data-Driven Phenotypic Categorization for Neurobiological Analyses: Beyond DSM-5 Labels

### Main Ideas

- Categorical definitions of illnesses are increasingly apparent
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
        - DSM-IV Axis I Disorders
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

