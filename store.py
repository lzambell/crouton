import config as cf
from tables import *
import numpy as np
import data_containers as dc


class Infos(IsDescription):
    date_start   = StringCol(8)
    hour_start   = StringCol(6)
    date_stop    = StringCol(8)
    hour_stop    = StringCol(6)
    n_files      = UInt16Col()
    n_events     = UInt32Col()
    n_muons      = UInt32Col()
    process_date = UInt32Col()
    t_first      = UInt32Col()
    t_last       = UInt32Col()
    delta_t      = UInt32Col()
    rate_all     = Float16Col()
    rate_muons   = UInt32Col()



def store_run_infos(h5file, now):
    table = h5file.create_table("/", 'infos', Infos, 'Run Infos')
    inf   = table.row

    inf['date_start']   = dc.the_run.date_ini
    inf['hour_start']   = dc.the_run.hour_ini
    inf['date_stop']    = dc.the_run.date_end
    inf['hour_stop']    = dc.the_run.hour_end
    inf['n_files']      = dc.the_run.n_files
    inf['n_events']     = dc.the_run.n_events
    inf['n_muons']      = dc.the_run.n_muons
    inf['t_first']      = dc.the_run.t_first
    inf['t_last']       = dc.the_run.t_last
    inf['delta_t']      = dc.the_run.run_dt
    inf['rate_all']     = dc.the_run.rate_all
    inf['rate_muons']   = dc.the_run.rate_muons
    inf['process_date'] = now
        
    inf.append()
    table.flush()


class Muons(IsDescription):
    tsamp = UInt32Col()
    tof   = Float16Col()
    theta = Float16Col()
    phi   = Float16Col()
    
    x_crt_top  = Float16Col()
    y_crt_top  = Float16Col()
    z_crt_top  = Float16Col()
    x_crt_bot  = Float16Col()
    y_crt_bot  = Float16Col()
    z_crt_bot  = Float16Col()
    x_LAr_in   = Float16Col()
    y_LAr_in   = Float16Col()
    z_LAr_in   = Float16Col()
    x_LAr_out  = Float16Col()
    y_LAr_out  = Float16Col()
    z_LAr_out  = Float16Col()


def store_muons(h5file):
    table = h5file.create_table("/", 'Muons', Muons, 'Reconstructed Muons')
    mu   = table.row
    for p in range(dc.the_run.n_muons):
        mu['tsamp'] = dc.data['time'][p]
        mu['tof']   = dc.data['tof'][p]
        mu['theta'] = dc.data['theta'][p]
        mu['phi']   = dc.data['phi'][p]
        
        mu['x_crt_top'] = cf.x_top
        mu['y_crt_top'] = dc.data['y_top'][p]
        mu['z_crt_top'] = dc.data['z_top'][p]

        mu['x_crt_bot'] = cf.x_bot
        mu['y_crt_bot'] = dc.data['y_bot'][p]
        mu['z_crt_bot'] = dc.data['z_bot'][p]

        mu['x_LAr_in'] = dc.data['vtx_in'][p][0]        
        mu['y_LAr_in'] = dc.data['vtx_in'][p][1]        
        mu['z_LAr_in'] = dc.data['vtx_in'][p][2]        

        mu['x_LAr_out'] = dc.data['vtx_out'][p][0]        
        mu['y_LAr_out'] = dc.data['vtx_out'][p][1]        
        mu['z_LAr_out'] = dc.data['vtx_out'][p][2]        
        
        mu.append()
    table.flush()
