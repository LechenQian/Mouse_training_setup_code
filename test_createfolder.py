import os

# define the name of the directory to be created
events_path = "C:/Users/MurthyLab/Desktop/Selina/experiment_data/C17/"

try:
    os.mkdir(events_path)
except OSError:
    print ("Creation of the directory %s failed" % events_path)
else:
    print ("Successfully created the directory %s " % events_path)