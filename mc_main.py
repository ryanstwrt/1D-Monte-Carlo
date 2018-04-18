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
print(len(geo.mesh))
# First loop loops over the number of total generations in the simulation
for i in range(0, int(kcode[1])):
    # Second for loop loops over the number of particles per generation
    print(i)
    k = 0
    for j in range(0, int(kcode[0])):
        # Generates a new particle each time
        p = su.gen_particle(kcode[3], i, mesh, cell_array, geo)
        # While loop continues to accumulate collisions while the particle is alive
        while p.alive:
            material = int(geo.mat[p.cell])
            xc = tr.get_XC(p.enrg, material, mat_array)
            tl_tot = tr.get_col_dist(xc.tot_xc)
            delta_x = tr.get_delta_x(p.dir, tl_tot)
            surf_cross = tr.det_surf_cross(delta_x, p, geo)

            # Particle does not undergo a collision, is simply reaches the
            # edge of the surface, gets tallied, and is sent off in a new
            # direction. This also determines if the particle encounters
            # a problem boundary, in our case the particle is reflected.
            if surf_cross:
                p.pos, dist2surf = tr.move_part2surf(p, geo, delta_x)
                tr_ln = tr.get_tr_ln(dist2surf, p.dir)
                if p.pos == geo.pos[0] or p.pos == geo.pos[-1]:
                    p.dir = -p.dir
            # If the particle does encounter a collision before the surface
            # then we sample to determine what type of collision occurs
            else:
                p.pos = tr.move_part(p, delta_x)
                tr_ln = tl_tot
                col_type = tr.get_col_type(xc, p.enrg)
                if col_type == 0:
                    p.alive = False
                elif col_type == 1:
                    pass
                else:
                    p.set_dir()
                    p.enrg = 2

            mesh_tally.accumulate(mesh_tally.mesh, p, tr_ln)
        k += 1
    mesh_tally.gen_flux(k, geo)
    print(mesh_tally.mesh)
    print(len(mesh_tally.mesh))

time1 = time.time()
print('1D MC took: ', time1-time0, 's to run.')