#running MGC between fmri and pfactor

#create distance matrix of pfactors
setwd("/Users/vidurkailash/")
y = as.matrix(read.table("fmri_pfactors.csv"), ncol = 1)
r = as.matrix(dist(y, method = "euclidean", diag = TRUE, upper = TRUE, p = 2))
View(r)

#read all edgelists and convert to list adjacency matrices
setwd("/Users/vidurkailash/ndmg_results//fmri/")
matrices <- list()
m <- 1
files <- list.files(path = "~/ndmg_results//fmri/")
for (f in 1:length(files)){
  cat("Reading file", f, "... ")
  g <- read.table(files[f])
  n <- sqrt(2*nrow(g))
  adj <- matrix( rep(0, n*n), nrow = n, ncol = n)
  for (k in 1:nrow(g)){
    i <- g[k,1]
    j <- g[k,2]
    adj[i,j] <- g[k,3]
    adj[j,i] <- g[k,3]
  }
  matrices[[m]] <- adj
  m <- m + 1
  cat("Adjacency matrix for file", f,"produced.\n")
}


#create distance matrix based on Frobenius norm of adjacency matrices
m <- length(matrices)
D <- matrix( rep(0, m*m), nrow = m )
D[1,1] <- 0
cat("Computed upper left 1 by 1 distance matrix.\n")
for (i in 2:m) {
  cat("Computed upper left", i, "by", i, "distance matrix.\n")
  D[i,i] <- 0
  for (j in 1:(i-1)) {
    diff_matrix <- matrices[[i]] - matrices[[j]]
    d <- norm(diff_matrix, type = c("F"))
    D[i, j] <- d
    D[j, i] <- d
  }
}

View(D)

#run MGC

require(mgc)
require(ggplot2)
require(latex2exp)
res <- mgc.test(r,D)
mgc.plot.plot_matrix(res$localCorr, title = TeX("MGC Corr Map, Pfactor and fMRI Connectomes"), legend.name=TeX("local corr"))
mgc.plot.plot_matrix(res$pLocalCorr, title = TeX("MGC Local P Corr Map, Pfactor and Connectomes"), legend.name=TeX("Pvalues"))
print(res$statMGC)
print(res$pMGC)
