data_path = "/eos/experiment/neutplatform/protodune/rawdata/np02/CRT/rootfiles"
store_path = "/eos/user/l/lzambell/analysis/crouton/reco"


n_paddles = 8
paddle_width = 144. #cm
paddle_height = 12. #cm

""" crt (top/bottom) positions in lardon coordinates [all in cm]"""
x_top = -580.99
x_bot =  580.99

""" values from the tree rounded """
z_top = [300.9, 315.1, 329.4, 343.7, 358.0, 372.3, 386.6, 400.8]
z_bot = [-207.5, -193.2, -178.9, -164.6, -150.3, -136.0, -121.7, -107.4]

""" tree coordinates along z have its origin at the center of the cryostat, need to shift to have it at the center of the LAr active volume """
z_shift = -45.2
z_top = [x + z_shift for x in z_top]
z_bot = [x + z_shift for x in z_bot]


""" LAr active volume position in cm (bounding box) """
x_min_lar = -300.
y_min_lar = -300.
z_min_lar = -300.
x_max_lar = 300.
y_max_lar = 300.
z_max_lar = 300.
