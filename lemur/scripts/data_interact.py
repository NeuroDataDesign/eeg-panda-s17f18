import os
import pickle

# After importing datasets into data folder of EEG (following HBNB dir format) and pickling some,
# import this function in order to get a dictionary of all available pickled data.
# Set sys.path.append('rel_path_to_this_script')

# EXAMPLE USAGE in Python:

# Import:
# import sys
# sys.path.append('../../../code/scripts')
# from data_interact import get_patient

# Use:
# patient = get_patient('NDARAA075AMK')

# function to get patient data
def get_patient(patient_num):
    # initialize patient
    patient = {}
    # set path to data
    patient_dir = "../../../data/" + patient_num + "/EEG/raw/PANDA"
    # iterate through available datasets for given patient
    for filename in os.listdir(patient_dir):
        if filename.endswith(".pkl"): 
            # get a relevant name for holding the data
            meta_name = filename.split("_")[1]
            meta_name = meta_name[0].lower() + meta_name[1:]
            # load the data
            patient[meta_name] = pickle.load(open(patient_dir + "/" + filename, "rb" ))
            continue
        else:
            continue
    return patient
    
