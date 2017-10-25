
# coding: utf-8
# USAGE: python get_data.py <modality> <release> <subject_index> <data-dir>

# Set up

import pandas as pd
import io
import requests
import boto3
import tarfile
import os
import pickle as pkl
import numpy as np
import multiprocessing
import sys
import shutil


paradigms = ["RestingState",
             "SAIIT_2AFC_Block1",
             "SAIIT_2AFC_Block2",
             "SAIIT_2AFC_Block3",
             "SurroundSupp_Block1",
             "SurroundSupp_Block2",
             "Video1",
             "Video2",
             "Video3",
             "Video4",
             "vis_learn",
             "WISC_ProcSpeed"]

MODALITY = sys.argv[1] # "MRI", "EEG"
RELEASE = sys.argv[2] # "R1","R2"
SUB_IDX = sys.argv[3] # subject index
OUT_BASE = sys.argv[4]
sub_url = "https://raw.githubusercontent.com/NeuroDataDesign/lemur-f17s18/master/data/allowed/%s_%s_Subjects.csv"
sub_url = sub_url % (MODALITY, RELEASE)

def getData(subject_id, paradigm):
    file_path = os.path.join(OUT_BASE, subject_id,
                             "EEG", "preprocessed", "csv_format",
                             subject_id + "_" + paradigm + "_data.pkl")
    if not os.path.isfile(file_path):
        print("Subject", subject_id, "did not have", paradigm, "file.")
        return None
    with open(file_path, "rb") as f:
        data = pkl.load(f)
        return data

def convData(tup):
    subject_id, paradigm = tup
    file_path = os.path.join(OUT_BASE, subject_id,
                             "EEG", "preprocessed", "csv_format",
                             subject_id + "_" + paradigm + "_data.csv")
    if not os.path.isfile(file_path):
        file_path = os.path.join(OUT_BASE, subject_id,
                                 "EEG", "preprocessed", "csv_format",
                                 paradigm + "_data.csv")
        if not os.path.isfile(file_path):
            print("Subject", subject_id, "did not have", paradigm, "file.")
            return
    data = np.loadtxt(file_path, dtype=np.float32, delimiter=",")
    #os.remove(file_path)
    new_path_base = os.path.join(OUT_BASE, "bids", subject_id)
    try:
        os.makedirs(new_path_base)
    except:  # Python >2.5
        pass
    new_path = os.path.join(new_path_base, subject_id + "_" + paradigm + "_data.pkl")
    with open(new_path, "wb") as f:
        pkl.dump(data.T, f)

content = requests.get(sub_url).content
string = io.StringIO(content.decode('utf-8'))
df = pd.read_csv(string, header=None)

subject_id = df.as_matrix()[int(SUB_IDX), 0]
file_name = "%s.tar.gz"%subject_id
local_path = os.path.join(OUT_BASE, file_name)
s3_path = "data/Projects/HBN/%s/%s/%s" % (RELEASE, MODALITY, file_name)
print("Copying from", s3_path, "to", local_path)

s3 = boto3.client('s3')
s3.download_file('fcp-indi', s3_path, local_path)

tar = tarfile.open(local_path, "r:gz")
tar.extractall(OUT_BASE)
tar.close()
os.remove(local_path)

pool = multiprocessing.Pool(multiprocessing.cpu_count())
args = zip([subject_id] * len(paradigms), paradigms)
pool.map(convData, args)
shutil.rmtree(os.path.join(OUT_BASE, subject_id))
