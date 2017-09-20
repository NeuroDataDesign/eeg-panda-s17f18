# Top visualizations for each modality
### Given n points in R^d
##### 1. For each dimension separately
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
##### 2. For all dimensions in aggregate
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
##### 3. Pairwise comparisons of dimensions
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
##### 4. Dimensionality reduced scatterplots
  * if real
    * 3d scatter of data projected onto subspace spanned by top 3 principal vectors
      * scree plot
    * 3d scatter of data t-sne'd
  * if categorical
    * 3d scatter of top 3 explanatory factors from EFA
    * Multiple Correspondence Analysis 3d scatter
    plot like this: ![](https://user-images.githubusercontent.com/10272301/30644718-4f86116a-9de1-11e7-9658-cbb5409984e0.png)
    or this: ![](https://user-images.githubusercontent.com/10272301/30644969-35411fc4-9de2-11e7-8fb9-971f4d4c9684.png)
      * scree plot
    
### EEG data (T points in R^d where T points are sequential sampled at some number of Hz)
##### 1. Visualize all signals, nonspatial
  * heatmap: ![](https://user-images.githubusercontent.com/10272301/30292624-e0f3e08e-9704-11e7-95a9-9b6570ccdfa7.png)
  * sparklines: ![](https://user-images.githubusercontent.com/10272301/30645401-a64c10ce-9de3-11e7-8bcf-b224d9457e9f.png)
##### 2. Visualize all signals, interpolated and spatial
  * spatially structured heatmap: ![](https://user-images.githubusercontent.com/10272301/30645736-9c0e1b74-9de4-11e7-8328-eb7a58d9ca30.png)
##### 3. Frequency domain information across all channels
  * heatmap where rows are channels, columns are time windows, values are fourier coefficients of certain frequency (allow user to vary the frequency)... (three dimensional?)
##### 4. Frequency domain information for each channel
  * spectrogram for each channel: maybe something nice like this? ![](https://user-images.githubusercontent.com/10272301/30646453-0eacb684-9de7-11e7-9be3-24abdb18564a.png)
  * wavelet coefficient decay plot: ![](https://user-images.githubusercontent.com/10272301/30646281-76a23bde-9de6-11e7-97b5-fe36edb00132.png)
##### 5. Dimensionality reduction time-series
  * color changing dynamical system plot of top 3 PCs
  * m-tsne ![](https://user-images.githubusercontent.com/10272301/30647696-1f209d5c-9dea-11e7-8478-17037768fa18.png)
