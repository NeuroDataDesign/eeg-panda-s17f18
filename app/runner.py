import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lemur import datasets as lds, metrics as lms, plotters as lpl, embedders as leb
from flask import Flask

def get_pheno_plots(target, file_path):
    pheno = lds.CSVDataSet(file_path,
                name = "HBN Phenotypic")
    pheno.imputeColumns("mean")
    return lpl.LocationHeatmap(pheno, mode='div').plot()

