import os
import pickle as pkl
import re
import pandas as pd
import sys
import json

FILENAME = "%s_%s_data.pkl"
FILENAMEREGEX = "^%s_(?P<task>.+)_data.pkl"
NOFILEERROR = "Subject %s did not have a %s task file."
SUBSTRING = "sub_%03d"
TASKSTRING = "task_%03d"
SUBERROR = "Invalid subject index %d for dataset with %d subjects."
TASKERROR = "Invalid task index %d for dataset with %d tasks."

class BIDSDataset:
    
    def __init__(self, base_path, dataset):
        self.base_path = base_path
        self.dataset = dataset

        self.raw_subjects = GetBIDSSubjects(self.base_path, self.dataset)
        self.subjects = [ SUBSTRING % (x) for x in range(len(self.raw_subjects)) ]
        self.subjects_map = dict(zip(self.subjects, self.raw_subjects))
        self.num_subjects = len(self.subjects)

        self.raw_tasks = GetBIDSTasks(self.base_path, self.dataset)
        self.tasks = [ TASKSTRING % (x) for x in range(len(self.raw_tasks)) ]
        self.tasks_map = dict(zip(self.tasks, self.raw_tasks))
        self.num_tasks = len(self.tasks)

        self.Meta = GetBIDSMeta(self.base_path, self.dataset)

    def getSubjectMap(self):
        d = {
            'raw': self.raw_subjects,
            'mine': self.subjects
        }
        D = pd.DataFrame(d)
        D.index.name = "index"
        return D

    def getTaskMap(self):
        d = {
            'raw': self.raw_tasks,
            'mine': self.tasks
        }
        D = pd.DataFrame(d)
        D.index.name = "index"
        return D

    def getSubject(self, sub):
        try:
            subject = self.subjects[sub]
        except:
            barf(SUBERROR % (sub, self.num_subjects))
        subject = self.subjects_map[subject]
        return subject

    def getTask(self, task):
        try:
            task = self.tasks[task]
        except:
            barf(TASKERROR % (sub, self.num_tasks))
        task = self.tasks_map[task]
        return task

    def getData(self, sub, task):
        subject = self.getSubject(sub)
        task = self.getTask(task)
        D = LoadBIDSData(self.base_path, self.dataset, subject, task)
        if self.Meta["dims_in_columns"]:
            D = D.T
        return D
        
def barf(string):
    print(string)
    sys.exit(1)

def GetBIDSMeta(base_path, dataset):
    file_path = os.path.join(base_path, "%s_meta.json" % (dataset))
    return json.load(open(file_path))

def LoadBIDSData(base_path, dataset, subject_id, task):
    file_path = os.path.join(base_path, dataset, subject_id, FILENAME % (subject_id, task))
    if not os.path.isfile(file_path):
        print(NOFILEERROR % (subject_id, task))
        return None
    with open(file_path, "rb") as f:
        data = pkl.load(f)
        return data

def GetBIDSSubjects(base_path, dataset):
    subjects = os.listdir(os.path.join(base_path, dataset))
    subjects.sort()
    return subjects

def GetBIDSTasks(base_path, dataset):
    subjects = GetBIDSSubjects(base_path, dataset)
    tasks = []
    for s in subjects:
        task_regex = FILENAMEREGEX % (s)
        file_names = os.listdir(os.path.join(base_path, dataset, s))
        for f in file_names:
            result = re.match(task_regex, f)
            tasks.append(result.group('task'))
    tasks = list(set(tasks))
    tasks.sort()
    return tasks

