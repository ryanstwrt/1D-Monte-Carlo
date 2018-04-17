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
    def set_cell(self, pos, cells, mat_pos):
        self.cell = ut.get_cell(pos, cells, mat_pos)
    def set_enrg(self):
        self.enrg = 1
    def set_dir(self):
        self.dir = ut.rand_dir()
    def set_alive(self):
        self.alive = True


# Creates a class for the geometry to easy obtain all relevent information
# regarding cells, mesh XC, etc.
class geometry:
    def set_mesh(self, mesh):
        self.mesh = mesh
    def set_cells(self, cell_array):
        self.cells = cell_array[:, 0]
    def set_pos(self, cell_array):
        self.pos = cell_array[:, 1]
    def set_mat(self, cell_array):
        self.mat = cell_array[:, 2]


# Creates a particle with a a set of unique characteristics
def gen_particle(keff, history, mesh, flux, geo):
    p = particle()
    p.set_wt(keff)
    p.set_pos(history, geo.pos, flux)
    p.set_cell(p.pos, geo.cells, geo.pos)
    p.set_enrg()
    p.set_dir()
    p.set_alive()
    return p


# Sets up the geometry from the information from the input file
def gen_geometry(mesh, cell_array):
    geo = geometry()
    geo.set_mesh(mesh)
    geo.set_mat(cell_array)
    geo.set_cells(cell_array)
    geo.set_pos(cell_array)
    geo.pos = np.append([0], geo.pos)
    return geo


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


# Reads in the input file and creates three separate vectors
# One vector for the geometry, one for the mesh and one for the kcode info
def input_reader(input_dir):
    with open(input_dir, "r") as file:
        # Figure out the number of cells in the problem
        num_cells = 0
        for i, line in enumerate(file):
            if line == "\n":
                break
            num_cells += 1

        # Write the cell array (forcing the cell array to start at 0.0)
        cell_array = np.zeros((num_cells, 3))
        file.seek(0)
        for i, line in enumerate(file):
            if line == "\n":
                break
            geo_line = [x for x in line.split(' ')]
            cell_array[i][0] = int(geo_line[0])
            cell_array[i][1] = cell_array[i-1][1] + float(geo_line[1])
            cell_array[i][2] = int(geo_line[2])

        # Write down the kcode information
        k_code = np.zeros(4)
        for i, line in enumerate(file):
            mat_line = [x for x in line.split(' ')]
            if i == 0:
                mesh_len = int(mat_line[1])
                mesh = np.arange(0, mesh_len)
            else:
                k_code[i-1] = float(mat_line[1])

        return cell_array, mesh, k_code
