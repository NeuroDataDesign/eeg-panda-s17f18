# Data-Driven Phenotypic Categorization for Neurobiological Analyses: Beyond DSM-5 Labels
Dam, O'Connor, Marcelle, Ho, Craddock, Tobe, Gabbay, Hudziak, Castellanos, Leventhal, Milham

### Main ideas
* Data driven methodologies can capture behavioral and biological variation
  which is not well explained by the current diagnostic categories.
* DSM-5 labels are useful for clinical application, but impede
  the search for patho-physiological markets
* The Research Doimain Criteria (RDoC) calls for a new nosology given the
  limitations of the current nosological systems. (See Insel TR 2014,
  The NIMH Research Domain Criteria (RDoC) Project.
* Fully dimensional perspectives on psychopathology have limited use 
  in clinical decision making
* Raises question: if new phenotypic targets were developed, should it
  be informed by previous models, data driven models, or both?
  * Maybe see Abernach System of Empirically Based Assessment
* Reiterates: consensus based system may provide valuable insights,
  but data driven approaches may be crucial for identifying more behaviorally 
  refined biologicaal phenotypes
* Uses a bootstrap based EFA model on the NKIRS sample
  (deeply phenotyped multimodal imaging dataset on adults)
  * on 49 subscales derived from 10 measures
* 6 factor model estimated with EFA, explains 77% of variance
* In this study, data driven approaches can yield clinically meaningful
  results with potentially important neurobiological differences.
  * Further research into data drive methods will require advanced methods
    and a large sample size, but this work at least shows that it is 
    possible to derive meaningful results using data driven approaches
    and supports further research.

### Dimensionalty Reduction
* For each patient, create phenotypic profile of 49 subscales
  (presumably x \in \mathbb{R}^49)
* Dimension reduction performed via EFA
* Maximum likelihood factor estimation with varimax rotation used to estimate
  six factor loadings for each subscale score
* 10000 bootstrapped resamplings

### What we could do
* This paper shows that it is quite possible and meaningful to
  use data driven approaches to seach for phenotypically 
  homogeneous groups of psychological conditions
* A limited range of algorithms were used for this goal, and
  for clustering. We could use more / better / more robust algorithms.
  * Seemed to be a complicate process to determine these groups,
    is there an even simpler way to explain a similar amount of variation?
    (78% for nonconstrained and 68% for constrained)
* Heirarchical clustering visualization in figure 2 is nice
* EFA factor profiles are really nice and would be awesome to automatically
  return to users in a webservice
* Further work can be done relating the neuroimaging data to these factors
  * Or at least, a way to visualize the likely high dimensional and highly
    nonlinear relationship
