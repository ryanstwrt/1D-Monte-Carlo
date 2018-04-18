import numpy as np
from random import *

# Get an initial random position based some upper and lower bound
def rand_init_pos(lower, upper):
    if lower > upper:
        print("FATAL ERROR: Lower bounds (%f) is greater than upper bounds (%f)." % (lower, upper))
        quit()
    pos = lower + (upper - lower) * random()
    return pos


# Sample from the fission source distribution
# To Do: Finish this!
def rand_pos(mesh, fission_src):
    if len(mesh) != len(fission_src):
        print("FATAL ERROR: The mesh size (%i) is not equal to the flux size (%i). " % (len(mesh), len(fission_src)))
        quit()
    norm_fission_src = fission_src / sum(fission_src)
    cum_fission_src = np.zeros_like(norm_fission_src)
    for i, src in enumerate(norm_fission_src):
        if i == 0:
            cum_fission_src[i] = src
        else:
            cum_fission_src[i] = src + cum_fission_src[i-1]
    sum_2 = sum(norm_fission_src)
    rand = random()
    ####To Do: Sample from the cumulative distribution!!
    #####
    for i, x in enumerate(pdf_tbl):
        print(pdf_tbl[i])
        if rand <= pdf_tbl[i]:
            cell = pdf_tbl[i]
            break
    return


# Get a random direction based on isotropic scattering/emission
def rand_dir():
    direction = 2 * random() - 1
    return direction


# Return a True if sigma_1 is sample and a False if not
def rand_col(sigma_1, sigma_t):
    if sigma_1 > sigma_t:
        print('FATAL ERROR: Sigma S (%f) is greater than Sigma T(%f)'
              'Check input file' % (sigma_1, sigma_t))
        quit()
    temp = sigma_1/sigma_t
    rand_temp = random()
    if rand_temp < temp:
        return True
    else:
        return False


# Grabs the cell number for the particle based on the defined mesh
def get_cell(pos, geo):
    if pos == geo.pos[0]:
        return geo.cells[0]
    elif pos == geo.pos[-1]:
        return geo.cells[-1]
    else:
        for i, x in enumerate(geo.cells):
            if geo.pos[i] <= pos < geo.pos[i+1]:
                return geo.cells[i]

