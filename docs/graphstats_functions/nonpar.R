# Load 'gmmase' package by Youngser Park <youngser@jhu.edu>.
if(!require(gmmase)){
  if (!require(devtools)) {
    install.packages("devtools")
    suppressMessages(require(devtools)) 
  }
  devtools::install_github("youngser/gmmase")
  suppressMessages(library(gmmase))
}

#' Nonparametric two-sample testing using kernel-based test statistic
#'
#' This is a simple implementation of the kernel-based test statistic for the nonparametric
#' two-sample testing problem of given \eqn{X_1, X_2, \dots, X_n} i.i.d. \eqn{F} and
#' \eqn{Y_1, Y_2, \dots, Y_m} i.i.d. \eqn{G}, test the null hypothesis of \eqn{F = G} against
#' the alternative hypothesis of \eqn{F \not = G}. The test statistic is based on embedding
#' \eqn{F} and \eqn{G} into a reproducing kernel Hilbert space and then compute a distance between
#' the resulting embeddings. For this primitive, the Hilbert space is associated with the
#' Gaussian kernel.
#'
#' @param Xhat1 a \eqn{n} x \eqn{d} matrix
#' @param Xhat2 a \eqn{n} x \eqn{d} matrix
#' @param sigma a bandwidth for the Gaussian kernel
#'
#' @return \code{T} A scalar value \eqn{T} such that \eqn{T} is near 0 if the rows of
#' \eqn{X} and \eqn{Y} are from the same distribution and \eqn{T} far from 0 if the rows of
#' \eqn{X} and \eqn{Y} are from different distribution.
#'
#' @author Youngser Park <youngser@jhu.edu>
#' @export
#' 
nonpar <- function(Xhat1, Xhat2, sigma=0.5) {
  
  return(nonpar(Xhat1,Xhat2,sigma))
  
}

# TO DO: Include code from R package, or leave the import in case the package is updated.