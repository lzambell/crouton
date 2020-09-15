import uproot
import numpy as np
import itertools

import data_containers as dc

class reader:
    """ reminder : add special case if file is corrupted or has no events """
    def __init__(self, name):

        self.n_files = len(name)

        self.trees = [x for x in uproot.iterate(name, "CRTtree")]
        self.n_events = sum([len(x[b'muon_flag']) for x in self.trees])

        self.t_first = self.trees[0][b'tstamp'][0]
        self.t_last  = self.trees[-1][b'tstamp'][-1]
        
        self.delta_t  = self.t_last - self.t_first

        dc.runs[-1].set_run_infos(self.t_first, self.t_last, self.n_events, self.n_files)


    def unpack(self, dict_name, branch_name):
        dc.data[dict_name] = np.asarray(list(itertools.chain.from_iterable([x[branch_name] for x in self.trees])))

    def get_all_events(self):
        self.unpack('time',  b'tstamp')
        self.unpack('y_top', b'Xtop')
        self.unpack('t_top', b'CFDtop')
        self.unpack('q_top', b'Qtop')
        self.unpack('y_bot', b'Xbot')
        self.unpack('t_bot', b'CFDbot')
        self.unpack('q_bot', b'Qbot')
        self.unpack('mu',    b'muon_flag')


        """
        #when only one file could be read
        ts, xt, tt, qt, xb, tb, qb, mu = self.tree.arrays(["tstamp", "Xtop", "CFDtop", "Qtop", "Xbot", "CFDbot", "Qbot", "muon_flag"], outputtype=tuple)

        dc.data['time']  = ts
        dc.data['y_top'] = xt
        dc.data['t_top'] = tt
        dc.data['q_top'] = qt
        dc.data['y_bot'] = xb
        dc.data['t_bot'] = tb
        dc.data['q_bot'] = qb
        dc.data['mu']    = mu
        """

        """ change position to cm and invert axis as in lardon """
        dc.data['y_top'] *= -1e2
        dc.data['y_bot'] *= -1e2


    def get_all_muons(self):
        self.get_all_events()
        for key, val in dc.data.items():
            sel = val[dc.data['mu']>=0]
            dc.data[key] = sel
        return len(dc.data['mu'])
