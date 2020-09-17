import config as cf
import numpy as np


data = {}

class run_info:
    def __init__(self):
        self.date_ini   = ""
        self.date_end   = ""
        self.hour_ini   = ""
        self.hour_end   = ""
        self.n_files    = 0
        self.run_dt     = -1
        self.n_events   = -1
        self.n_muons    = -1
        self.t_first    = -1        
        self.t_last     = -1
        self.rate_all   = -1.
        self.rate_muons = -1.
        
    def set_run_name(self, date_ini, date_end, hour_ini, hour_end):
        """ from the file name """
        self.date_ini = date_ini
        self.hour_ini = hour_ini
        self.date_end = date_end
        self.hour_end = hour_end


    def set_run_infos(self, t_first, t_last, n_events, n_files):
        """ from reading the tree """
        self.t_first  = t_first
        self.t_last   = t_last
        self.run_dt   = t_last - t_first
        self.n_events = n_events
        self.n_files  = n_files

    def set_n_muons_and_rate(self, n_muons):
        self.n_muons = n_muons
        
        self.rate_all   = self.n_events/self.run_dt
        self.rate_muons = self.n_muons/self.run_dt

    def dump(self):
        print("\n* - * - * - * - * - * - * - * - * - * - * - * - ")
        print(" Run analyzed from ", self.date_ini, " to ", self.date_end)
        print(" Processed hours from ", self.hour_ini, " to ", self.hour_end)
        print(" -> ", self.n_files, " file(s)")
        print(" 1st event : ", self.t_first, " Last : ", self.t_last)
        print(" Elapsed time: ", self.run_dt, "s")
        print(" Nb of triggered events: ", self.n_events)
        print("* - * - * - * - * - * - * - * - * - * - * - * - \n")
        
the_run = run_info()
