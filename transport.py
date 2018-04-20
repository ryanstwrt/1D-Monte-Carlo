import utils as ut
import numpy as np
from random import *

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
    prev_cell = p.cell
    if new_pos >= geo.pos[p.cell+1]:
        if p.cell == geo.cells[-1]:
            part_pos = geo.pos[-1]
            dist2surf = part_pos - p.pos
        else:
            part_pos = geo.pos[p.cell+1]
            dist2surf = part_pos - p.pos
            p.set_cell(part_pos, geo)
    else:
        if p.cell == geo.cells[0]:
            part_pos = geo.pos[0]
            dist2surf = p.pos - part_pos
        else:
            part_pos = geo.pos[p.cell-1]
            dist2surf = p.pos - part_pos
            p.set_cell(part_pos, geo)
    return part_pos, dist2surf, prev_cell


# Determine the tracklength if the particle encountered a surface
def get_tr_ln(delta_x, mu):
    tr_ln = abs(delta_x / mu)
    return tr_ln

# Returns 0 for absorption, 1 for inscatter, 2 for downscatter
def get_col_type(XC, erng):
    sigma_f = XC.fiss_xc / XC.tot_xc
    sigma_i = XC.inscat_xc / XC.tot_xc + sigma_f
    sigma_d = XC.downscat_xc / XC.tot_xc + sigma_i
    rand = random()
    if rand < sigma_f:
        return 0
    elif rand < sigma_i:
        return 1
    else:
        return 2

