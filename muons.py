import config as cf
import data_containers as dc
import ray_tracer as rt

import numpy as np
import math


def extract_muon():
    """ keep only the informations on the muons """
    """ from LPSC : mu = (i_top)*10 + i_bot """

    """ T->B Time of Flight """
    time_t = [x[int((y-y%10)/10)] for x,y in zip(dc.data['t_top'],dc.data['mu']) if y>=0]
    time_b = [x[y%10] for x,y in zip(dc.data['t_bot'],dc.data['mu']) if y>=0]
    dc.data['tof'] = [b-t for t,b in zip(time_t,time_b)]

    
    """ get z t/b position of muons """
    dc.data['z_top'] = [cf.z_top[int((y-y%10)/10)] for y in dc.data['mu'] if y>=0]
    dc.data['z_bot'] = [cf.z_bot[y%10] for y in dc.data['mu'] if y>=0]

    dx = np.array([cf.x_bot-cf.x_top for x in dc.data['mu'] if x>=0])
    dy = np.array([x[z%10] - y[int((z-z%10)/10)] for x,y,z in zip(dc.data['y_bot'], dc.data['y_top'], dc.data['mu']) if z>=0])
    dz = np.array([x-y for x,y in zip(dc.data['z_bot'], dc.data['z_top'])])

    dc.data['theta'] = np.degrees(np.arctan2( np.sqrt(dx**2 + dy**2), dz))
    dc.data['phi']   = np.degrees(np.arctan2(dy, dx)) 



    """ get only the positions of mu in each paddles """
    """ event correlation is lost in these arrays! """
    dc.data['y_top_pad'] = [[x[int((y-y%10)/10)] for x,y in zip(dc.data['y_top'],dc.data['mu']) if y>=0 and int((y-y%10)/10)==z] for z in range(cf.n_paddles)]
    dc.data['y_bot_pad'] = [[x[y%10] for x,y in zip(dc.data['y_bot'],dc.data['mu']) if y>=0 and y%10==z] for z in range(cf.n_paddles)]


    
    """ get y t/b position of muons """
    dc.data['y_top'] = [x[int((y-y%10)/10)] for x,y in zip(dc.data['y_top'], dc.data['mu']) if y>=0]
    dc.data['y_bot'] = [x[y%10] for x,y in zip(dc.data['y_bot'],dc.data['mu']) if y>=0]


    """ get the (x,y,z) in and out vertices in the LAr fiducial volume """
    bot_lar_fid = rt.Vector3([cf.x_min_lar, cf.y_min_lar, cf.z_min_lar])
    top_lar_fid = rt.Vector3([cf.x_max_lar, cf.y_max_lar, cf.z_max_lar])
    box = rt.Box(bot_lar_fid, top_lar_fid)
    

    v3top = [rt.Vector3([cf.x_top,y,z]) for y,z in zip(dc.data['y_top'], dc.data['z_top'])]
    v3bot = [rt.Vector3([cf.x_bot,y,z]) for y,z in zip(dc.data['y_bot'], dc.data['z_bot'])]

    rays = [rt.Ray(t,b) for t,b in zip(v3top, v3bot)]
    in_lar = [box.intersect(r, 0, 10e6) for r in rays]

    if(len(in_lar)-sum(in_lar) !=0):
        print(" --> ", len(in_lar)-sum(in_lar), " muon(s) triggered not in LAr Fid. Volume")

    dc.data['vtx_in'] = [box.get_point_in(r) if fv is True else [-999., -999., -999.] for r,fv in zip(rays, in_lar)]
    dc.data['vtx_out'] = [box.get_point_out(r) if fv is True else [-999., -999., -999.] for r,fv in zip(rays, in_lar)]
