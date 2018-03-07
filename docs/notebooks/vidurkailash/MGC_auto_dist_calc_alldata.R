#Pfactor Distance Matrix
y = matrix( c(1.631981049, 1.985156054, 1.324180567, 1.906069835, 1.971683558))
r = dist(y, method = "euclidean", diag = TRUE, upper = TRUE, p = 2)
r

#Incidence Edgelist to Adjacency Matrix
os <- list()
m <- 1
files <- list.files(path = "~/edgelists/")
for (f in 1:length(files)){
  cat("Reading file", f, "... ")
  g <- read.table(files[f])
  n <- sqrt(2*nrow(g))
  o <- matrix( rep(0, n*n), nrow = n, ncol = n)
  for (k in 1:nrow(g)){
    i <- g[k,1]
    j <- g[k,2]
    o[i,j] <- g[k,3]
    o[j,i] <- g[k,3]
  }
  os[[m]] <- o
  m <- m + 1
  cat("Adjacency matrix for file", f,"produced.\n")
}

#Connectome Distance Matrix 
m <- length(os)
D <- matrix( rep(0, m*m), nrow = m )
D[1,1] <- 0
cat("Computed upper left 1 by 1 distance matrix.\n")
for (i in 2:m) {
  cat("Computed upper left", i, "by", i, "distance matrix.\n")
  D[i,i] <- 0
  for (j in 1:(i-1)) {
    diff_matrix <- os[[i]] - os[[j]]
    d <- norm(diff_matrix, type = c("F"))
    D[i, j] <- d
    D[j, i] <- d
  }
}

View(D)

#Run MGC on 2 Distance Matrices 
require(mgc)
require(ggplot2)
require(latex2exp)
mgc.test(r,D)
res <- mgc.test(r,D) 
mgc.plot.plot_matrix(res$localCorr, title = TeX("MGC Corr Map, Pfactor and Connectomes"), legend.name=TeX("local corr"))
print(res$optimalScale)
print(res$statMGC)

