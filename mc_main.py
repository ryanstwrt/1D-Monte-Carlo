import set_up as su
import transport as tr
import tally as tal
import plotter as plot
import time


print("Welcome to the 1D Monte Carlo Slab solver!\n")
print("Starting Simulation Now")
time0 = time.time()
data_file = "TestA.txt"
input_file = "Input_File.txt"

mat_array = su.get_data(data_file)
cell_array, mesh, kcode = su.input_reader(input_file)
geo = su.gen_geometry(mesh, cell_array)
tally = tal.init_track_length_tally(geo)
k_tally = tal.init_k_tally(kcode)
# First loop loops over the number of total generations in the simulation
for i in range(0, int(kcode[1])):
    # Second for loop loops over the number of particles per generation

    k = 0
    test = 0
    test2 = 0

    for j in range(int(kcode[0])):
        # Generates a new particle each time
        if i == 0:
            p = su.gen_particle(k_tally.k_tally[i], i, cell_array, geo)
        else:
            p = su.gen_particle(k_tally.k_tally[i], i, tally.fission_source, geo)

        # While loop continues to accumulate collisions while the particle is alive
        while p.alive:

            material = int(geo.mat[p.cell])
            xc = su.get_XC(p.enrg, material, mat_array)
            tl_tot = tr.get_col_dist(xc.tot_xc)
            delta_x = tr.get_delta_x(p.dir, tl_tot)
            surf_cross = tr.det_surf_cross(delta_x, p, geo)

            # Particle does not undergo a collision, is simply reaches the
            # edge of the surface, gets tallied, and is sent off in a new
            # direction. This also determines if the particle encounters
            # a problem boundary, in our case the particle is reflected.
            if surf_cross:
                p.pos, dist2surf, prev_cell = tr.move_part2surf(p, geo, delta_x)
                tr_ln = tr.get_tr_ln(dist2surf, p.dir)
                if p.pos == geo.pos[0] or p.pos == geo.pos[-1]:
                    p.dir = -p.dir
                tally.accumulate(p, prev_cell, tr_ln)
                tally.accumulate_current(p.cell, prev_cell, p.enrg)
                tally.accumulate_mesh(p, tr_ln)

            # If the particle does encounter a collision before the surface
            # then we sample to determine what type of collision occurs
            else:
                p.pos = tr.move_part(p, delta_x)
                tr_ln = tl_tot
                tally.accumulate(p, p.cell, tr_ln)
                tally.accumulate_mesh(p, tr_ln)
                col_type = tr.get_col_type(xc, p.enrg)
                if col_type == 0:
                    p.alive = False
                elif col_type == 1:
                    p.set_dir()
                else:
                    p.enrg = 2
                    p.set_dir()

        k += 1

    print(test, test2)
    # Clear the previous generations flux/fission source to make room for the new flux
    # and fission source
    tally.clear_fission_source()
    tally.clear_flux()

    # Generate the flux and fission source for this generation
    tally.gen_flux(k, geo)
    tally.gen_fission_source(geo, mat_array)

    # Now that we have generated our new flux/fission source, erase the tracklength tally
    tally.clear_track_length()
    if i < k_tally.num_gen:
        print(k_tally.k_tally[i])
        new_k = k_tally.get_k(k_tally.k_tally[i], geo, tally.fission_source)
        k_tally.accumulate_k(i+1, new_k)

    plot.plot_flux(tally.current)
    plot.plot_flux(tally.flux)
    plot.plot_flux(tally.fission_source)
    plot.plot_flux(tally.mesh)
    if i > 98:
        plot.plot_flux(tally.flux)
        plot.plot_flux(tally.fission_source)
    tally.clear_current()
    tally.clear_mesh()

time1 = time.time()
print('1D MC took: ', time1-time0, 's to run.')