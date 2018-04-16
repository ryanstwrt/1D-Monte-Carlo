import utils as ut
import numpy as np
from random import *

class XC():
    def get_tot_xc(self, enrg, material, mat_array):
        if enrg == 1:
            self.tot_xc = mat_array[material][1]
        else:
            self.tot_xc = mat_array[material][7]

    def get_inscat_xc(self, enrg, material, mat_array):
        if enrg == 1:
            self.inscat_xc = mat_array[material, 2]
        else:
            self.inscat_xc = mat_array[material, 8]

    def get_downscat_xc(self, enrg, material, mat_array):
        if enrg == 1:
            self.downscat_xc = mat_array[material, 3]
        else:
            self.downscat_xc = mat_array[material, 9]

    def get_fiss_xc(self, enrg, material, mat_array):
        if enrg == 1:
            self.fiss_xc = mat_array[material, 4]
        else:
            self.fiss_xc = mat_array[material, 10]

    def get_nu(self, enrg, material, mat_array):
        if enrg == 1:
            self.nu = mat_array[material, 5]
        else:
            self.nu = mat_array[material, 11]

    def get_xi(self, enrg, material, mat_array):
        if enrg == 1:
            self.xi = mat_array[material, 6]
        else:
            self.xi = mat_array[material, 12]


# Get a random path length traveled based on Transport XC
def get_col_dist(sigma_t):
    col_dist = - np.log(random()) / sigma_t
    return col_dist


# Get the delta_x travelled in the system
def get_delta_x(mu, col_dist):
    if -1 >= mu <= 1:
        print('FATAL ERROR: Scattering angle %f was not within bounds of -1 to 1' % mu)
        quit()
    delta_x = - mu * col_dist
    return delta_x

#def det_surf_cross(delta_x, p, geo):
