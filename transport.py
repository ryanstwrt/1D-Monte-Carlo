import utils as ut
import numpy as np
import set_up as su
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


# create a XC set for the current particle
def get_XC(enrg, material, mat_array):
    xc = XC()
    xc.get_tot_xc(enrg, material, mat_array)
    xc.get_downscat_xc(enrg, material, mat_array)
    xc.get_inscat_xc(enrg, material, mat_array)
    xc.get_fiss_xc(enrg, material, mat_array)
    xc.get_nu(enrg, material, mat_array)
    xc.get_xi(enrg, material, mat_array)
    return xc


# Get a random path length traveled based on Transport XC
def get_col_dist(sigma_t):
    col_dist = - np.log(random()) / sigma_t
    return col_dist


# Get the delta_x travelled in the system
def get_delta_x(mu, col_dist):
    if -1 >= mu <= 1:
        print('FATAL ERROR: Scattering angle %f was not within bounds of -1 to 1' % mu)
        quit()
    delta_x = mu * col_dist
    return delta_x


# Determine if a the particle has crossed a surface
def det_surf_cross(delta_x, p, geo):
    new_pos = p.pos + delta_x
    if new_pos >= geo.pos[p.cell+1] or new_pos < geo.pos[p.cell]:
        return True
    else:
        return False


# If the particle has not moved outside the cell, simply move the particle
# to the new position and do not update the cell
def move_part(p, delta_x):
    new_pos = p.pos + delta_x
    return new_pos


# If the particle has moved to a surface, move the particle to the surface and
# update the cell the particle is currently in
def move_part2surf(p, geo, delta_x):
    new_pos = p.pos + delta_x
    if new_pos >= geo.pos[p.cell+1]:
        part_pos = geo.pos[p.cell+1]
        dist2surf = part_pos - p.pos
    else:
        part_pos = geo.pos[p.cell]
        dist2surf = p.pos - part_pos
    if part_pos == p.pos:
        pass
    p.set_cell(part_pos, geo)
    return part_pos, dist2surf


# Determine the tracklength if the particle encountered a surface
def get_tr_ln(delta_x, mu):
    tr_ln = abs(delta_x / mu)
    return tr_ln

# Returns 0 for absorption, 1 for inscatter, 2 for outscatter
def get_col_type(XC, erng):
    sigma_s = XC.downscat_xc + XC.inscat_xc
    col_type = ut.rand_col(sigma_s, XC.tot_xc)
    if not col_type:
        return 0
    else:
        scat_type = ut.rand_col(XC.inscat_xc, sigma_s)
        if scat_type:
            return 1
        else:
            return 2
