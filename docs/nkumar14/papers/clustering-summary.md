

## Multidimensional Scaling

- Means of visualizing level of similarity of individual cases of a dataset
- Non-linear dimensionality reduction
- Between object distances preserved as much as possible
- Each object is assigned coordinates in each of N dimensions **(choosen as an a priori)**
  - PCA (choose the components that produce the most variety as principal ones)
  - Metric MDS: superset of classical MDS that generalizes optimization procedure to a variety of MDS functions
  - Non-metric MDS: non-parametric monotonic relationship between similarities in item-item matrix and Euclidean distances between items
    - Minimize a stress function that relates point distances to a transformation function
    - 2-fold optimization: find optimal transformation and then points have to be arranged so distances match scaled proximities

## Hierarchical Clustering

- **Agglomerative (bottom up):** each observation starts in its own cluster, and pairs of clusters are merged as one moves up the hierarchy
- **Divisive (top down):** all observations start in one cluster, splits performed recursively into multiple clusters

## t-SNE

- Nonlinear dimensionality reduction technique for high-dimensional data to 2-3 dimensions visualizable in a scatter plot
- **2 Steps:**
  - **1:** Probability distribution over pairs of high-dimension objects so similar objects have higher prob of being picked
  - **2:** Creates prob dist over points in a low-dimensional map and minimizes KL divergence between 2 distributions
- Can use any distance metric
- Kind of like Gaussian Kernel Density Estimation... similarity of point *i* to point *j* in the conditional prob that *i* would pick *j* as its neighbor if there was a gaussian centered at *i*

### KL-Divergence

- Relative entropy
- Measures distance between 2 distributions
- Does so by checking the "randomness" of 2 distributions and comparing them
- **Asymmetric**
