import uproot
import numpy as np

import data_containers as dc

class reader:
    """ reminder : add special case if file is corrupted or has no events """
    def __init__(self, name):
        self.crt_file = uproot.open(name)
        self.tree     = self.crt_file['CRTtree']
        self.n_events = self.tree.numentries
        self.t_first  = self.tree.array("tstamp", 
                                        entrystart = 0, 
                                        entrystop  = 1)[0]
        
        self.t_last   = self.tree.array("tstamp", 
                                        entrystart = self.n_events-1, 
                                        entrystop  = self.n_events)[0]

        self.delta_t  = self.t_last - self.t_first

        dc.runs[-1].set_run_infos(self.t_first, self.t_last, self.n_events)

    def get_all_events(self):
        ts, xt, tt, qt, xb, tb, qb, mu = self.tree.arrays(["tstamp", "Xtop", "CFDtop", "Qtop", "Xbot", "CFDbot", "Qbot", "muon_flag"], outputtype=tuple)

        dc.data['time']  = ts
        dc.data['y_top'] = xt
        dc.data['t_top'] = tt
        dc.data['q_top'] = qt
        dc.data['y_bot'] = xb
        dc.data['t_bot'] = tb
        dc.data['q_bot'] = qb
        dc.data['mu']    = mu

        """ change position to cm and invert axis as in lardon """
        dc.data['y_top'] *= -1e2
        dc.data['y_bot'] *= -1e2

    def get_all_muons(self):
        self.get_all_events()
        for key, val in dc.data.items():
            sel = val[dc.data['mu']>=0]
            dc.data[key] = sel
        return len(dc.data['mu'])
