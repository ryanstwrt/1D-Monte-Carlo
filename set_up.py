import utils as ut
import numpy as np

# Creates a class for the particle which contains the particles weight,
# position, cell, energy (where energy 1 is fast), and direction
class particle:
    '''Creates a class for the particle'''
    def set_wt(self, keff):
        self.wt = keff
    def set_pos(self, history, mesh, flux):
        if history == 0:
            self.pos = ut.rand_init_pos(mesh[0], mesh[-1])
        else:
            self.pos = ut.rand_pos(mesh, flux)
    def set_cell(self, pos, mesh):
        self.cell = ut.get_cell(pos, mesh)
    def set_enrg(self):
        self.enrg = 1
    def set_dir(self):
        self.dir = ut.rand_dir()


# Creates a particle with a a set of unique characteristics
def gen_particle(keff, history, mesh, flux):
    p = particle()
    p.set_wt(keff)
    p.set_pos(history, mesh, flux)
    p.set_cell(p.pos, mesh)
    p.set_enrg()
    p.set_dir()
    return p


#class geometry(mesh, mat_array):
 #   def mesh(self):
 #       self.mesh = mesh
 #   def material(self):
 #       self.mat = get_geometry()
 #   def sigma_t(self, mat_array):
 #       self.sigma_t_1 = mat_array


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

geom_dir = "Input_File.txt"


def get_geometry(geom_dir):
    with open(geom_dir, "r") as file:
        # Figure out the number of cells in the problem
        num_cells = 0
        for i, line in enumerate(file):
            if line == "\n":
                break
            num_cells += 1

        # Write
        cell_array = np.zeros((num_cells, 3))
        file.seek(0)
        for i, line in enumerate(file):
            if line == "\n":
                break
            geo_line = [x for x in line.split(' ')]
            if i == 0:
                cell_array[i][1] = float(geo_line[1])
            else:
                cell_array[i][1] = cell_array[i-1][1] + float(geo_line[1])
            cell_array[i][0] = geo_line[0]
            cell_array[i][2] = geo_line[2]


    return

get_geometry(geom_dir)

mesh = flux = np.arange(0, 4)

p = gen_particle(1.0, 0, mesh, flux)
