**EEG Visualizations, incorporating spatial metadata with temporal data:**

- Sparklines
  - Raw sparklines
    - Highlight specific *bad* ones (not really necessary becasue of preprocessing)
  - Average over sets of electrodes
    - Decided by location metadata
    - Decided by location metadata and correlation of electrode activity (evaluated by some clustering metric)
  - Separate by event triggers, place side by side
  - Separate by spikes not associated with events?
  - Separate by frequency bands
- Spectrograms
  - Raw spectrogram
  - Separate by frequency bands
    - Draw lines separating within the full spectrogram to make comparison easier
    - Specific zoom ins of each band
- Heatmaps
  - Raw Frequency + Time
  - Wavelet Coefficients
  - Symlog again?
  - Head shaped heat map
    - 3D
    - Different planes (using location metadata)
  - CCA, PCA, M-TSNE to obtain linear combinations of electrodes that we can represent with both regular and head shaped heatmaps
- Correlation and Coherence Matrix
  - Time correlations
  - Correlations after clustering into functional units
  - For specific frequency bands
  
  **EEG-Categorical Ideas (for when we have phenotypic):**
  
  Currently empty!
