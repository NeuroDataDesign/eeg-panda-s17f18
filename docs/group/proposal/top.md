# Top visualizations for each modality
### Given n points in R^d
1. For each dimension separately
  * if categorical
    * show unique values
    * bar plot distribution (ordered if ordinal)
    * polychoric/polyserial correlation, then use real
  * if real
    * show distribution (bar plot categorical, kde real valued)
      * interval estimate of mean
      * outliers in red
    * ecdf and cdf of fit gaussian
      * arrow at argmax abs( ecdf(x) - cdf(x) )
2. For all dimensions in aggregate
  * if categorical
    * distribution of
      * number of categories
      * modes, frequency of mode
      * entropy based on categorical distribution
  * if real
    * distribution of
      * ks statistics
      * means
      * std. devs
      * kurtosis
3. Pairwise comparisons of dimensions
  * if real
    * pearson correlation matrix
    * coherence matrix (if signal)
    * pairplot
  * if categorical
    * paired counts heatmaps?
      * for each dimension pair (x, y), heatmap where rows are
        possibilities for x, colums possibilities for y, color by
        number of samples for which possibility pair is present
