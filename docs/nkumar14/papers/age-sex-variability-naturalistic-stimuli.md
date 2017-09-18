# Age and sex modulate the variability of neural responses to naturalistic videos 

### Main Ideas

- Investigated influence of age and sex on responses to naturalistic video stimuli
    - First EEG study to report a measure of across-subject nerual similarity with clear age and sex effects
- Large sample (N = 114) and then replicated in independent cohort (N = 303)
- **Significance:**
    - As age increased, neural responses were more variable
    - Females responded more variably than males (a difference that disappeared with age)
    - Results consistent with theories variability increases with maturation and  that neural maturation occurs earlier in females
- Neural variability increases because increase in neural complexity
- **Slight Paradox:** neural variability does not imply proficient behavior; specific metrics are more variable in children. These are more measurable through *fMRI*

### Experiment & Setup

- EEG was recorded as they were presented with borth naturalistic and converntional stimuli
- **Neural Variability** measured with **inter-subject correlation (ISC)** of responses evoked by stimuli
        - ISC of the EEG is indicative of attention, engagement, and memory in healthy adults
- Subjects
    - N = 144: 6 to 44 years old (14.2 +/- 8.0 years old, 46 females)
    - N = 303: 5 to 21 years old (11.3 +/- 3.9 years old, 135 females)
- Stimuli:
    - Fun with Fractals
    - How to improve at Simple Arithmetic
    - Pre-Algebra Class
    - Diary of a Wimply Kid trailer
    - Despicable Me
- Baseline ISC established by 4m 20s eyes-closed rest period

### Procedure

- 128 channel EEG headset, 500 Hz sample
- Preprocessing
    - Downsampled to 125 Hz
    - High-pass filtered at 1 Hz
    - Notch Filtered @ 59-61 Hz w/ 4th Order Butterworth Filter
    - Eye artifacts removed by linearly regressing EOG channels from scaled EEG channels
    - Robust PCA (inexact Augmented Lagrange Multipliers Method) removed sparse outliers from the data
    - Some removed by visual inspection

### Inter-Subject Correlation (ISC)

- Used extensively in BOLD signal in fMRI
- Asseses level of correlation in EEG amongst group of subject as they respond to same stimulus
- ISC utilizes correlated component analysis (CCA) to identify linear combinations of EEG electrodes that capture most correlation
    - CCA is like PCA except maximizes correlation as opposed to variance

### Steady State Visual Evoked Potentials (SSVEPs)

- To determine baseline strength of SSVEPs for individuals, used a flashing light paradigm to get a baseline for evoked potentials

### Results

#### ISC and Varying Stimuli

- ISC will indicate varying levels of engagement
- Average ISC measured across each stimulus:
    - Wimpy: 0.053 +/- 0.036
    - DesMe: 0.035 +/- 0.023
    - Arith: 0.019 +/- 0.013
    - Fract: 0.026 +/- 0.016
    - StudT: 0.012 +/- 0.009
    - Flash: 0.030 +/- 0.019
    - Rest: 0.001 +/- 0.004
- ISC went up for more engaging videos like Wimpy and DesMe, and in the educational videos was highest for Fract an educational video focused on shapes

#### ISC Decreases with Age

- ISC is computed by measuring similarity to others in same stimulus condition
- All stimuli negative relationship between age and ISC
    - ISC did not vary with age during rest
- Because components that maximize correlation across all subjects, and there are more young subject, chosen components may be biased towards them
    - Thus recalculated after splitting into groups with an even split
- For all stimuli, negative relationship remained
- [Picture here]

#### ISC Correlation Elevated in Males

- Gender differences in ISC correlation is largely significant at younger ages (supporting hypotheses that females neurally mature faster than males)
- [Picture here]


