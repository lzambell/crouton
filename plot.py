import config as cf
import data_containers as dc

import matplotlib.pyplot as plt
import colorcet as cc 
import matplotlib as mpl
import matplotlib.gridspec as gridspec


"""define default color cycle from colorcet"""
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=cc.glasbey_category10)



def plot_run_summary(option=None):
    fig = plt.figure(figsize=(12,8) )
    gs  = gridspec.GridSpec(nrows=4, ncols=6)

    ax_ytop = fig.add_subplot(gs[0, 1:4])
    ax_ytop.hist(dc.data['y_top_pad'], 150, range=(50, 250),label=['paddle '+str(i) for i in range(8)], stacked=True)
    #ax_ytop.legend()
    ax_ytop.set_xlabel('y top position [cm]')

    ax_ybot = fig.add_subplot(gs[1, 1:4])
    ax_ybot.hist(dc.data['y_bot_pad'], 150, range=(50, 250), label=['paddle '+str(i) for i in range(8)], stacked=True)
    #ax_ybot.legend()
    ax_ybot.set_xlabel('y bottom position [cm]')

    ax_leg = fig.add_subplot(gs[0:2, 0])
    ax_leg.legend(*ax_ybot.get_legend_handles_labels(), loc='center')
    ax_leg.axis('off')
    
    
    ax_ztop = fig.add_subplot(gs[0, 4:])
    zt = [int((x-x%10)/10) for x in dc.data['mu'] if x>=0]
    ax_ztop.hist(zt, 8, range=(0, 7), histtype="step")
    ax_ztop.set_xlabel('top panels')                             

    ax_zbot = fig.add_subplot(gs[1, 4:])
    zb = [x%10 for x in dc.data['mu'] if x>=0]
    ax_zbot.hist(zb, 8, range=(0, 7), histtype="step")
    ax_zbot.set_xlabel('bottom panels')                             
    
    ax_tof = fig.add_subplot(gs[2:,0:2])
    ax_tof.hist(dc.data['tof'], 125, range=(38, 48), log=True )
    ax_tof.set_xlabel('time of flight [ns]')
    
    ax_ang = fig.add_subplot(gs[2:, 2:])
    ax_ang.hist2d(dc.data['phi'], dc.data['theta'], bins=[15,15],cmap=cc.cm.linear_tritanopic_krjcw_5_95_c24_r, range=[[-8.035, 8.035], [109.187, 117.636]])
    ax_ang.set_xlabel('phi [deg]')                             
    ax_ang.set_ylabel('theta [deg]')                             

    date_nice = dc.runs[-1].date_ini[:4]+"/"+dc.runs[-1].date_ini[4:6]+"/"+dc.runs[-1].date_ini[6:]
    fig.suptitle(date_nice+ ": Ntot = "+str(dc.runs[-1].n_events)+" [%.2f Hz]"%(dc.runs[-1].rate_all)+", Nmu = "+str(dc.runs[-1].n_muons)+" [%.2f Hz]"%(dc.runs[-1].rate_muons))
    fig.subplots_adjust(top=0.92, bottom=0.08, left=0.06, right=0.98, hspace=0.45, wspace=0.45)
    
    if(option):
        option = "_"+option
    else:
        option = ""

    plt.savefig("plot/run_control_"+dc.runs[-1].date_ini+".png")
    #plt.show()
    plt.close()
    
