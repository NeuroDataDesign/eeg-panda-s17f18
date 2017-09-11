# Downloading_data.md
#### How to download data from the HBNB (Healthy Brain Network Biobank).

# Phenotypic data
* Some small publicilly available phenotypic data here: http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/_files/HBN_S1_Pheno_data.csv
~Follow instructions under LORIS here: http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/sharing_phenotypic.html#loris
You can try the COINS Data Catalog too, but the HBN data did not seem to be listed there for some reason.~

# EEG
* Direct Download: http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/downloads_EEG.html
* AWS: http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/sharing_neuro.html#aws-and-cyberduck
* Pipeline Documentation: https://github.com/NeuroDataDesign/orange-panda-f16s17
* Raw electrode locations: https://raw.githubusercontent.com/fieldtrip/fieldtrip/master/template/electrode/GSN-HydroCel-128.sfp
* Mapping of electrodes to 10-20 system names: https://www.egi.com/images/HydroCelGSN_10-10.pdf

* Using the download script in this repo (9/11 Deliv)
1. clone this repo.
2. find a patient id here: https://github.com/NeuroDataDesign/eeg-panda-s17f18/blob/master/data/allowed/subject_ids.csv
  * Note! Not all will work or are in the final set
3. run `./code/scripts/HBNB_download.sh -sub (subject-id) -o data/`
4. (With python 2 activated) run `./code/scripts/HBNB_to_PANDA.sh -i data/(subject-id)/EEG/raw/csv_format/(subject-id)_(task)_data.csv -o data/output/file/location/output.pkl`

# MRI
* Direct: http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/downloads_MRI.html
* AWS: http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/sharing_neuro.html#aws-and-cyberduck
* Pipeline Documentation: https://github.com/NeuroDataDesign/fngs-f16s17
