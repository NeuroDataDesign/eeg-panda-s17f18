if(!require(igraph)){
  install.packages("igraph")
  suppressMessages(require(igraph))
}

#' Laplacian Spectral Embedding (LSE)
#'
#' \code{lse} provides the embedding of an laplacian matrix in a lower-dimensional eigenspace.
#'
#' @param g The igraph graph object.
#' @param dim The number of dimensions to project onto.
#' @return The |V| x dim embeded laplacian matrix.
#' @export
#'
lse <- function(g, dim) {
  
  # Input validation.
  if (class(g) == "dgCMatrix") { g = igraph::graph_from_adjacency_matrix(g) }
  if (class(g) != 'igraph') { stop("Input object 'g' is not an igraph graph.") }
  if (!is.integer(dim)) { stop("Input 'dim' must be an integer.") }
  if (dim > g.vcount()) { stop("Number of dimensions 'dim' is greater than number of vertices.") }

  X <- embed_laplacian_matrix(g, dim)$X
  return(X)
}