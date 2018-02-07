#' @title Visualize data using MEDA package from NeuroData.io
#' @author Ronak Mehta

# User input: Set to path of the subject's CSV file, and select fields to down sample by.
subject_file <- "../Desktop/NeuroData/NDARAA075AMK_RestingState_data.csv"

# User input: Down sample fields.
first_obs_no <- 1
last_obs_no <- 100001
sep <- 50

# Do not edit below.
require(data.table)
require(meda)

# Set the columns (observations) we want to take.
columns <- seq(first_obs_no, last_obs_no, sep)

# Set column names to the electrodes.
col_names <- rep("E", 128)
for (i in 1:length(col_names)) { col_names[i] <- paste(col_names[i], as.character(i), sep = "") }

# Injest CSV of subject's data.
if(FALSE) {
dat <- transpose(fread(input = subject_file, 
                                sep = ",", 
                                nrows = 128,
                                header = FALSE,
                                showProgress = TRUE,
                                select = columns,
                                data.table = FALSE))
colnames(dat) <- col_names
}
# Plot exploratory analyses.

# Location plots
plot(mlocation(dat))

# Heat Map
print(plot(d1heat(dat)))

# Outlier Plot
print(plot(outliers(dat)))

# Correlation Matrix
plot(medacor(dat))

# Cumulative Variance Plot
print(plot(cumvar(dat)))

# Fit Clusters with GMM
h <- hmc(dat)

# Dendogram
plotDend(h)

# Stacked Cluster Means Plot
print(stackM(h, centered = TRUE))

# Cluster Means
clusterMeans(h)


