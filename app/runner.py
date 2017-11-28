import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from lemur import datasets as lds, metrics as lms, plotters as lpl, embedders as leb

def get_pheno_plots(target, file_path):
    pheno = lds.CSVDataSet(file_path,
                index_column = "Identifiers",
                column_level_names = ("Instrument", "Variable"),
                name = "Phenotypic")
    lpl.EverythingPlotter(pheno).plot(target, lpl.ColumnDistributionPlotter)
