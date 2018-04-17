import set_up as su
import utils as ut
import transport as tr
import tally
import time


print("Welcome to the 1D Monte Carlo Slab solver!\n")
print("Starting Simulation Now")
time0 = time.time()
data_file = "TestA.txt"
input_file = "Input_File.txt"

mat_array = su.get_data(data_file)
cell_array, mesh, kcode = su.input_reader(input_file)
geo = su.gen_geometry(mesh, cell_array)
mesh_tally = tally.init_mesh_tally(geo)
# First loop loops over the number of total generations in the simulation
for i in range(0, int(kcode[1])):
    # Second for loop loops over the number of particles per generation
    for j in range(0, int(kcode[0])):
        # Generates a new particle each time
        p = su.gen_particle(kcode[3], i, mesh, cell_array, geo)
        # While loop continues to accumulate collisions while the particle is alive
        k = 0
        while p.alive:
            xc = tr.get_XC(p.enrg, int(cell_array[p.cell, 2]), mat_array)
            tl_tot = tr.get_col_dist(xc.tot_xc)
            delta_x = tr.get_delta_x(p.dir, tl_tot)
            dist_moved, surf_cross = tr.det_surf_cross(delta_x, p, geo)
            # Particle does not undergo a collision, is simply reaches the
            # edge of the surface, gets tallied, and is sent off in a new
            # direction. This also determines if the particle encounters
            # a problem boundary, in our case the particle is reflected.
            if surf_cross:
                tr.move_part2surf(p, geo, delta_x)
                tr_ln = tr.get_tr_ln(dist_moved, p.dir)
                if p.pos == cell_array[0, 1] or p.pos == cell_array[0, -1]:
                    p.dir = -p.dir
                else:
                    p.set_dir()

            # If the particle does encounter a collision before the surface
            # then we sample to determine what type of collision occurs
            else:
                tr.move_part(p, dist_moved)
                tr_ln = tl_tot
                col_type = tr.get_col_type(xc, p.enrg)
                if col_type == 0:
                    p.alive = False
                elif col_type == 1:
                    p.set_dir()
                else:
                    p.set_dir()
                    p.enrg = 2
            mesh_tally.accumulate(mesh_tally.mesh, p, tr_ln)
            k += 1
    #print(mesh_tally.mesh)

time1 = time.time()
print('1D MC took: ', time1-time0, 's to run.')