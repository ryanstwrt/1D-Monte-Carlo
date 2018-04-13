import numpy as np
from random import *

test_case = "TestA.txt"


# Read in the data from the different test cases
def get_data(test_case):
    with open(test_case, "r") as file:
        # determine the number of rows needed
        num_row = int(sum(1 for x in file)-1)
        file.seek(0)
        # determine the number of columns needed
        for line in file:
            num_col = int(sum(1 for x in line.split(' ')))
        # Return to the top of the file and step through each line
        # Then pull the data in each line and place it in a matrix
        # Which will have the form
        file.seek(0)
        mat_array = np.zeros((num_row, num_col))
        for i, line in enumerate(file):
            if i == 0:
                pass
            else:
                mat_line = [x for x in line.split(' ')]
                for x in range(len(mat_line)):
                    if x == 0:
                        pass
                    else:
                        mat_array[i-1][x] = mat_line[x]
        return mat_array


# Get an initial random position based some upper and lower bound
def rand_init_pos(lower, upper):
    if lower > upper:
        print("FATAL ERROR: Lower bounds (%f) is greater than upper bounds (%f)." % (lower, upper))
        quit()
    pos = lower + (upper - lower) * random()
    return pos


# Sample from the flux distribution
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
    return


# Get a random direction based on isotropic scattering/emission
def rand_dir():
    direction = 2 * random() - 1
    return direction


# Get a random path length traveled based on Transport XC
def rand_dist(mu, sigma_t):
    if -1 >= mu <= 1:
        print('FATAL ERROR: Scattering angle %f was not within bounds of -1 to 1' % mu)
        quit()
    dist = - mu * np.log(random()) / sigma_t
    return dist


# Return a 0 on scatter and a 1 on absorption
def rand_col(sigma_s, sigma_t):
    if sigma_s > sigma_t:
        print('FATAL ERROR: Sigma S (%f) is greater than Sigma T(%f)'
              'Check input file' % (sigma_s, sigma_t))
        quit()
    temp = sigma_s/sigma_t
    rand_temp = random()
    if rand_temp < temp:
        return 0
    else:
        return 1


# Grabs the cell number for the particle based on the defined mesh
def get_cell(pos, mesh):
    for i, x in enumerate(mesh):
        if i > 0:
            if mesh[i-1] < pos < mesh[i]:
                return i-1
            else:
                pass
