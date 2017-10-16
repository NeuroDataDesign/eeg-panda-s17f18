import os
import pickle as pkl

def getData(subject_id, paradigm):
    file_path = os.path.join("..", "..", "..", "data", subject_id,
                             "EEG", "preprocessed", "csv_format",
                             subject_id + "_" + paradigm + "_data.pkl")
    if not os.path.isfile(file_path):
        print(print("Subject", subject_id, "did not have", paradigm, "file."))
        return None
    with open(file_path, "rb") as f:
        data = pkl.load(f)
        return data
