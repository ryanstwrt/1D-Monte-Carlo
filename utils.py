import numpy as np
from random import *

# Get an initial random position based some upper and lower bound
def rand_init_pos(lower, upper):
    if lower > upper:
        print("FATAL ERROR: Lower bounds (%f) is greater than upper bounds (%f)." % (lower, upper))
        quit()
    pos = lower + (upper - lower) * random()
    return pos


# Sample from the flux distribution
# To Do: Finish this!
def rand_pos(mesh, flux):
    if len(mesh) != len(flux):
        print("FATAL ERROR: The mesh size (%i) is not equal to the flux size (%i). " % (len(mesh), len(flux)))
        quit()
    pdf_tbl = np.zeros_like(flux)
    for i, x in enumerate(flux):
        if i == 0:
            pdf_tbl[i] = x
        else:
            pdf_tbl[i] = x + pdf_tbl[i-1]
    pdf_sum = sum(pdf_tbl)
    for i, x in enumerate(flux):
        pdf_tbl[i] /= pdf_sum
        print(pdf_tbl[i])
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
def get_cell(pos, cells, mat_pos):
    for i, x in enumerate(cells):
        if i > 0:
            if mat_pos[i-1] < pos < mat_pos[i]:
                return int(cells[i]-1)
            else:
                pass
