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
      * entropy
  * if real
    * distribution of
      * ks statistics
      * means
      * std. devs
      * kurtosis
