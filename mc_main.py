import set_up as su
import utils as ut
import transport as tr
import tally


print("Welcome to the 1D Monte Carlo Slab solver!\n")
data_file = "TestA.txt"
input_file = "Input_File.txt"

mat_array = su.get_data(data_file)
cell_array, mesh, kcode = su.input_reader(input_file)
geo = su.gen_geometry(mesh, cell_array)
print("Starting Simulation Now")
# First loop loops over the number of total generations in the simulation
XC = tr.XC();
for i in range(0, int(kcode[1])):
    # Second for loop loops over the number of particles per generation
    for j in range(0, int(kcode[0])):
        # Generates a new particle each time
        p = su.gen_particle(kcode[3], i, mesh, cell_array, geo)
        # While loop continues to accumulate collisions while the particle is alive
        k=0
        while k < 10:
            tr.XC.get_tot_xc(XC, p.enrg, int(cell_array[p.cell, 2]), mat_array)
            col_dis = tr.get_col_dist(XC.tot_xc)
            print(col_dis)

            k += 1
