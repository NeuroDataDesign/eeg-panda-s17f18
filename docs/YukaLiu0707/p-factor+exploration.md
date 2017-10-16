
# Derivation of p factor scores
(https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5636639/)

- confirmatory factor analysis of self-report and diagnostic interview measures of internalizing, externalizing, and thought disorder symptoms
    - using the weighted least squares means and variance adjusted (WLSMV) algorithm
        - The WLSMV estimator is appropriate for categorical and nonmultivariate normal data and provides consistent estimates when data are missing at random with respect to covariates
- extracted using regression method: mean = 100, SD = 15
- use MPlus compare different structural models of the psychiatric symptoms (https://www.statmodel.com/examples/index.shtml)
- internalizing symptoms: five scores of anxiety and depressive symptoms were created: 
    - a MASQ-SF anxiety score was created by standardizing (z-scoring) and then averaging the Anxious Arousal and General Distress scales; 
    - the sum total score on the STAI-T self-report questionnaire was used as a second measure of trait anxiety; 
    - a MASQ-SF depression score was created by z-scoring and averaging the Anhedonic Depression and General Distress Depression scales; 
    - the sum total score on the CESD scale was used as a second measure of depression; 
    - e-M.I.N.I. symptom counts of social phobia, panic disorder, and agoraphobia were z-scored and then averaged to create a count of fears/phobias symptoms!
- externalizing symptoms: five scores of antisocial personality/psychopathy and substance abuse and dependence symptoms were created
- thought: Three scores of obsessive-compulsive disorder, mania, and psychosis were created
- three possible models:
    - correlated factors model
    - bi-factor model
    - one factor model
    - *accessed using chi-square value, the comparative fit index (CFI), the Tucker-Lewis index (TLI), and the root-mean square error of approximation (RMSEA)*
    - p-factor was extracted through standard regression method

# structual correlates to 'p' factor
- negative correlation with white matter integrity within bilateral pons (indexed by lower FA values)
- GMV: higher p factor scores -> significantly less volume of gray matter within the right and left lingual gyrus, right intracalcarine cortex of the occipital lobe and left posterior cerebellum
- whole-brain functional connectome
    - relationship between p factor scores and the whole-brain intrinsic connectivity of nodes in visual association cortex
- MDMR found four regions of interest:  left lingual gyrus, right middle occipital gyrus, and two adjacent parcels of the left middle occipital gyrus

https://github.com/mattcieslak/easy_lausanne 

program used in p-factor paper with a prerequisite of FreeSurfer, which we have tested and prefer not to use.

----------------------Method to investigate whole-brain connectivity in p-factor paper--------------------------------

# CWAS(connectome-wide association studies)
- using resting state fMRI
https://fcp-indi.github.io/docs/developer/_modules/CPAC/cwas/utils.html#calc_cwas


- **seed-based connectivity map**: 

reference: https://github.com/FCP-INDI/C-PAC/blob/master/CPAC/sca/sca.py

Seed-based Correlation Analysis (SCA) is one of the most common ways to explore functional connectivity within the brain. Based on the time series of a seed voxel (or ROI), connectivity is calculated as the correlation of time series for all other voxels in the brain. The result of SCA is a connectivity map showing Z-scores for each voxel indicating how well its time series correlates with the time series of the seed. Below is an example connectivity map showing correlated voxels based on a seed in the precuneus
    - extract a seed time series using Time Series Extraction
    - compute voxel-wise correlation with Seed Timeseries
    - normalized to contain Z-scores （the number of standard deviations from the mean a data point is）via Fisher R to Z transform

- **average distance between each pair of participant’s functional connectivity map**
    - 1 - correlation computed above

- **Multivariate Distance Matrix Regression(MDMR)**: (reveal connectivity in visual cortex)

reference: https://fcp-indi.github.io/docs/developer/_modules/CPAC/cwas/mdmr.html#mdmr
    - compute Gower's centered matrix
    - calculate MDMR statistics for the voxel
    - determine significance of MDMR statistics with permutation tests
    

# Basic simulation
If the correlations between p-factor and those structual correlates are reliable, we could perform analysis on them and see if we could notice something that imply high p factor scores. We need more information on what features our data have to further investigate the basic simulation setting.


# Possible application in our data
P-factor was calculated out using scores extracted from questionnaire (5 for internalizing and externalizing, 3 for thought) through model-fitting (using MPlus). Since we do not have those questionnaires, it would be hard to replicate the "p-factor" scores.
Another possible approach is that we could look at ROIs that have strong correlations with p-factor score (white matter volume, gray matter and whole-brain intrinsic connectivity)

