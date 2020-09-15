import uproot
import numpy as np
import sys
import glob
import time

import config as cf
import data_containers as dc
import reader as read
import muons as ana_mu
import plot as plot


def need_help():
    print("Usage: python crouton.py ")
    print(" TO ANALYSE ONLY ONE FILE (=one day)")
    print(" -date <crt data taking date as YYYYMMDD e.g. 20200904> ")
    print(" TO ANALYSE MULTIPLE FILES (=several days) not yet implemented")
    print("-from <YYYYDDMM> -to <YYYYMMDD>")
    print(" -n <number of event to process>  [default (or -1) is all]")
    print(" to have an output h5 file with all muons infos ")
    print(" -out <output name (optional though)>")
    print(" -h print this message")

    sys.exit()

    

if len(sys.argv) == 1:
    need_help()
else:
    for index, arg in enumerate(sys.argv):
        if arg in ['-h'] :
            need_help()


outname_option = ""
nevent  = -1
date = ""
do_store = False
for index, arg in enumerate(sys.argv):
    if arg in ['-date'] and len(sys.argv) > index + 1:
        date = sys.argv[index + 1]
    elif arg in ['-n'] and len(sys.argv) > index + 1:
        nevent = int(sys.argv[index + 1])
    elif arg in ['-out'] :
        do_store = True
        if len(sys.argv) > index + 1:
            outname_option = sys.argv[index + 1]



if(len(date)==0):
    print("CRT data taking day is mandatory ! ")
    need_help()

#print(date)

t_start = time.time()

data_path = cf.data_path+"/CRT_"+date+"*.root"
files = glob.glob(data_path)

if(len(files) == 0):
    print("no file available on ", date, ", sorry")
    sys.exit()

dc.runs.append(dc.run_info())

if(outname_option):
    outname_option = "_"+outname_option
else:
    outname_option = ""
    
name_out = cf.store_path + "/" + date + outname_option + ".h5"
print("output file : ", name_out)
output_mess = "not" if do_store is False else ""
print("-> will "+output_mess+" store output file")

""" change so that one can also read multiple files """
#print("file(s) found : [will read the 1st one only now]")
#print(files)

day_ini  = files[0][-20:-12]
hour_ini = files[0][-11:-5]

day_end  = files[-1][-20:-12]
hour_end = files[-1][-11:-5]
n_files = len(files)
reading = read.reader(files[0])

dc.runs[-1].set_run_name(day_ini, day_end, hour_ini, hour_end, n_files)
dc.runs[-1].dump()

""" to get all events """
#reading.get_all_events()

""" to get only muon-like events """
n_muons = reading.get_all_muons()
dc.runs[-1].set_n_muons_and_rate(n_muons)


""" clean mu-like events, and compute extra things (tof, theta, phi) """
ana_mu.extract_muon()
print(" time to open and extract muons: %.3f s"%(time.time()-t_start))
plot.plot_run_summary()
#sys.exit()

