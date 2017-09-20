# Top visualizations for each modality
### Given n points in R^d
1. For each dimension
  * if categorical
    * show unique values
    * bar plot distribution (ordered if ordinal)
  * if real
    * show distribution (bar plot categorical, kde real valued)
      * interval estimate of mean
      * outliers in red
    * ecdf and cdf of fit gaussian
      * arrow at argmax abs( ecdf(x) - cdf(x) )
