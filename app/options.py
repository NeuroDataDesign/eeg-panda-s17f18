#'NameOfPlotInLemur': 'name-of-plot-file-name'
aggregate_options = {
    'pheno': {
        'heatmap': ('Heatmap', 'Heatmap', 'heatmap'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'eeg': {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'fmri': {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'graph': {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree'),
        'gr_stats': ('Graph Stats', 'GraphStats', 'gr_stats')
    }
}

# EEG and FMRI One-to-One options.
one_to_one_options = {
    'pheno' : {
    },
    'eeg' : {
        'connectedscatter': ('Connected Scatter', 'ConnectedScatterplot', 'connectedscatter'),
        'sparkline': ('Sparkline', 'SparkLinePlotter', 'sparkline'),
        'spatialtimeseries': ('Spatial Time Series', 'SpatialTimeSeries', 'spatialtimeseries'),
        'spatialpgram': ('Spatial Periodogram', 'SpatialPeriodogram', 'spatialpgram')
    },
    'fmri' : {
        'orth_epi': ('Time Elapse of fMRI Signal', 'TimeElapse', 'orth_epi')
    },
    'graph' : {
        'gr_stats': ('Graph Stats', 'GraphStats', 'gr_stats')
    }
}

# Embed for EEG and FMRI
embedded_options = {
    'pheno' : {
        'heatmap': ('Heatmap', 'Heatmap', 'heatmap'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat' : ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree' : ('Scree Plot', 'ScreePlotter', 'scree'),
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat')
    },
    'eeg' : {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'fmri' : {
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'squareheat': ('Heatmap', 'Heatmap', 'squareheat'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    },
    'graph' : {
        'heatmap': ('Heatmap', 'Heatmap', 'heatmap'),
        'histogramheat': ('Histogram Heatmap', 'HistogramHeatmap', 'histogramheat'),
        'locationlines': ('Location Lines', 'LocationLines', 'locationlines'),
        'locationheat': ('Location Heatmap', 'LocationHeatmap', 'locationheat'),
        'correlation': ('Correlation Matrix', 'CorrelationMatrix', 'correlation'),
        'evheat': ('Eigenvector Heatmap', 'EigenvectorHeatmap', 'evheat'),
        'scree': ('Scree Plot', 'ScreePlotter', 'scree')
    }
}

clustering_options = {
    'pheno' : {
        'hgmmscmh' : ('HGMM Stacked Cluster Means Heatmap',
                      'ClusterMeansLevelHeatmap',
                      'hgmmscmh'),
        'hgmmcmd' : ('HGMM Cluster Means Dendrogram',
                     'HierarchicalClusterMeansDendrogram',
                     'hgmmcmd'),
        'hgmmcpp' : ('HGMM Pairs Plot',
                     'ClusterPairsPlot',
                     'hgmmcpp'),
        'hgmmcmll' : ('HGMM Cluster Means Level Lines',
                      'ClusterMeansLevelLines',
                      'hgmmcmll'),
        'hgmmcmlh' : ('HGMM Cluster Means Level Heatmap',
                      'HierarchicalStackedClusterMeansHeatmap',
                      'hgmmcmlh')
    },
    'eeg' : {
    },
    'fmri' : {
    },
    'graph' : {
        'hgmmscmh' : ('HGMM Stacked Cluster Means Heatmap',
                      'ClusterMeansLevelHeatmap',
                      'hgmmscmh'),
        'hgmmcmd' : ('HGMM Cluster Means Dendrogram',
                     'HierarchicalClusterMeansDendrogram',
                     'hgmmcmd'),
        'hgmmcpp' : ('HGMM Pairs Plot',
                     'ClusterPairsPlot',
                     'hgmmcpp'),
        'hgmmcmll' : ('HGMM Cluster Means Level Lines',
                      'ClusterMeansLevelLines',
                      'hgmmcmll'),
        'hgmmcmlh' : ('HGMM Cluster Means Level Heatmap',
                      'HierarchicalStackedClusterMeansHeatmap',
                      'hgmmcmlh')
    }
}
