if(!require(mclust)){
  install.packages("mclust")
  suppressMessages(library(mclust))
}

#' Select number of mixture components for Gaussian Mixture Model.
#'
#' \code{glust} selects optimal number of mixture components to describe data. 
#'
#' @param X A matrix object with n rows (data points) by d columns (dimensions).
#' @param K=2 The maximum number of components to be considered. Model selected from 1 to K components. 
#' @return The optimal number of cluster components. 
#'
gclust <- function(X, K=2) {
  
  # Input validation
  if (!is.matrix(X)) { stop("Input 'X' is not a matrix.")}
  if (!is.integer(K)) { stop("Input 'K' must be an integer.") }
  if (K < 1) { stop("Input 'K' must be greater than 1.") }
  
  # Fit model and retrieve optimal cluster number.
  return(Mclust(X, 1:K)$G)
}