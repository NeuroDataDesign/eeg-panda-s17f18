# Top visualizations for each modality
### Given n points in R^d
1. For each dimension separately
  * if categorical
    * show unique values
    * bar plot distribution (ordered if ordinal)
    * polychoric/polyserial correlation, then use real
    * whatever this plot is called:
    ![](https://user-images.githubusercontent.com/10272301/30643415-d1d1691c-9ddc-11e7-849c-f821dd35e8d9.png)
  * if real
    * show distribution (bar plot categorical, kde real valued)
      * interval estimate of mean
      * outliers in red
    * ecdf and cdf of fit gaussian
      * arrow at argmax abs( ecdf(x) - cdf(x) )
      ![](https://user-images.githubusercontent.com/10272301/30643594-991d4086-9ddd-11e7-8715-c658761fe19a.png)
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
    * pairplot:
    ![](https://user-images.githubusercontent.com/10272301/30644052-1f22d366-9ddf-11e7-98ec-c53528e7ed06.png)
  * if categorical
    * cramer's v matrix
    ![](https://user-images.githubusercontent.com/10272301/30643852-740b95a8-9dde-11e7-999a-a0ab2b129c74.png)
    * or even better, with clustering:
    ![](https://user-images.githubusercontent.com/10272301/30643929-b3a0dd0e-9dde-11e7-81fc-c86fa816c78e.png)
