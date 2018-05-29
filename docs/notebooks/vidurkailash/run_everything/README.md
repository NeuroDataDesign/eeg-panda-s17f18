In this 'run everything' folder, there is code that was used to run NDMG (using MARCC) and PANDAS (using ec2) on the HBN 
dataset. 

Files starting with 'mgc_' are R scripts used to run MGC on pfactors and the different neuroimaging modalities. 

In order to run MGC, two nxn distance matrices are necessary for input. The first matrix is a distance matrix based on the
pfactors. The second matrix is a distance matrix of the frobenius norms of either the correlation matrices produced from 
PANDAS of the adjacency matrices produced from NDMG. 

The same n=175 was used for running MGC on pfactor and EEG/fMRI/dMRI. Although the entire HBN dataset has 900 individuals, n could only be a max of 175 after cross checking between all modalities and pfactors. Only 175 individuals had EEG, fMRI, dMRI, and pfactor data. 

That being said, there are also MGC plots available based on each individual modality and total available data for each. 

EEG: n = 694
fMRI: n = 304
dMRI: n = 271
