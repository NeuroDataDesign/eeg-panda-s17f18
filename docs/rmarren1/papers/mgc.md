# Discovering Relationships and their Structures Across Disparate Data Modalities
Cencheng Shen, Carey E. Priebe, Mauro Maggioni, Qing Wang, Joshua T Vogelstein

### Main Ideas
* Most current statictical tests do not work well for data that is high dimensional, highly non-linear, and has small sample size.
* MGC (Multiscale Generalized Correlation) takes a multi-scale resolution approach to solving this problem.
* MGC generalizes (and theoretically dominates) its global counterparts. E.g., if there exists a global test which will find a dependence, MGC can find that same dependence with the same number or fewer samples

### Explanatory example?
* Consider a relationship between two variables (X, Y) in two geometric relationships, linear and a spiral.
  * A simple test taking into account globally all pairwise distances will detect the strong relationship in the linear case, but will not in the spiral case.
  * Why? The spiral has nonlinear local structure that cannot be captured globally!
  * MGC takes into account local structures by only considering pairwise distances of some number of nearest points (all numbers of nearest points, but all are computed and the best is returned).
  * somewhat similar intuitively to n-dimensional wavelets

### Algorithmic considerations
* O(N^2logn / T) where T is number of processors (parallel implementations)
  * not too bad for our use case (n~700)
* open source, implemented in R and Matlab
  * maybe make a wrapper for R
* Very good pseudocode in the back of the paper
  * possible to implement ourselves if absolutely needed

### Possible extensions / uses for our project
* can probably be extended by nice visualizations
  * visualize nearest neighbor distribution per dimension, or in pairs?
  * visualize number of nearest neighbors per dimension (lower number = more nonlinear dependence on that dimension, higher number = less nonlinear)
* domain specific visualizations
  * colorize voxels in MRI by number of nearest neighbors
    * same for eeg?
* A *very* good way to test whether a relationship exists between 
  high dimensional neuroimaging data and some numerical value representing
  a phenotypic variable (maybe even relate to the p-factor)
  * same for ordinal values to be related to p-factor, if we can get a
    real-value representation of ordinal fields (method from p-factor paper)

