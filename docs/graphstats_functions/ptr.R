# Load 'gmmase' package by Youngser Park <youngser@jhu.edu>.
if(!require(gmmase)){
  if (!require(devtools)) {
    install.packages("devtools")
    suppressMessages(require(devtools)) 
  }
  devtools::install_github("youngser/gmmase")
  suppressMessages(library(gmmase))
}
if(!require(igraph)){
  install.packages("igraph")
  suppressMessages(library(igraph))
}

#' Run pass-to-rank on a weighted graph.
#'
#' It extracts (non-zero) edge weight vector \eqn{W} from a graph and replaces it with \eqn{2*R / (|E|+1)} where \eqn{R} is the rank of \eqn{W} and \eqn{|E|} is the number of edges. This does 'no-op' for an unweighted graph.
#'
#' @param g A graph in \code{igraph} format or an n x 2 edge list or an n x n adjacency matrix
#' @return The modified graph object.
#' @author Youngser Park <youngser@jhu.edu>
#' @export
#' @import igraph
ptr <- function(g) {
  
  #  Validate input.
  if (class(g) == "dgCMatrix") { g = igraph::graph_from_adjacency_matrix(g) }
  if (class(g) != 'igraph') { stop("Input object 'g' is not an igraph graph.") }
  
  g <- ptr(g)
  out <- as.matrix(g[])
  return(out)
}