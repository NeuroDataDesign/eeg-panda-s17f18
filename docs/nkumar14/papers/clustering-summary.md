

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


## [Network Clustering Methods](https://arxiv.org/pdf/1508.04757.pdf)

- **FG: Fast Greedy Algorithm (like Kruskal's)**
  - All edges removed, each node is considered a community
  - Figure out which edge would most increase ***[modularity](https://en.wikipedia.org/wiki/Modularity_(networks))***
  - Edge inserted and merge communities
  - Continues till all communities are merged
  - Choose iteration with highest modularity
- **WT: Walktrap (a lot like Diffusion Maps???)**
  - Each node gets a probability distribution representing probability of reaching other nodes based on some distance metric
  - Merge communities with similar prob distributions
- **LP: Label Propagation**
  - Each vertex gets a label
  - Random walk, each vertex gets label with highest occurence of neigbors
  - Algorithm converges when each vertex has the same label as majority of its nieghbors

#### Basic pipeline of implementing clustering methods

1. Normalization: pre-processed scaling
2. Distance measures: calculate distance matrix
3. Network Construction: use some method (like k-NN)
4. Community Detection: use one of the algos

## DBSCAN

- Points are classified as *core points,* *(density-)reachable points,* and *outliers*
  - Core points: at least *minPts* points within distance *eps*. All points within *eps* are *directly reachable* from *p*. Cannot be directly reachable from a non-core point.
  - *q* is directly reachable from *p* if there exists a path *p_1, p_2, ... p_i, p_{i+1}, ... q.* Where all *p_{i + 1}* are directly reachable from *p_i*.
  - All points not reachable from any other points that are outliers
- **Density connectedness:** *p* and *q* are connected if both are reachable from *o*. This metric is symmetric.
- **2 parameters:** *minPts*, *eps*
