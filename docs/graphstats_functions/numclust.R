#' Number of Clusters
#' 
#' \code{numclust} Select the number of clusters.
#' @param X [m, n] Data matrix.
#' @return Number of clusters.
#' @export
#'
numclust <- function(X)
{
  out <- which.max(X)
  return(out)
}