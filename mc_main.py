import set_up as su
import transport as tr
import tally as tal
import post_process as pp
import numpy as np
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
    test = 0
    test2 = 0
    cell_check = np.zeros(1001)
    for j in range(int(kcode[0])):
        # Generates a new particle each time
        if i == 0:
            p = su.gen_particle(k_tally.k_tally[i], i, cell_array, geo)

        else:
            p = su.gen_particle(k_tally.k_tally[i], i, tally.fission_source, geo)
        cell_check[j] = p.cell

        # While loop continues to accumulate collisions while the particle is alive
        while p.alive:

            material = int(geo.mat[p.cell])
            xc = su.get_XC(p.enrg, material, mat_array)
            tl_tot = tr.get_col_dist(xc.tot_xc)
            delta_x = tr.get_delta_x(p.dir, tl_tot)

            surf_cross = tr.det_surf_cross(delta_x, p, geo)

            # Particle does not undergo a collision, is simply reaches the
            # edge of the surface, gets tallied, and is sent off in a the same
            # direction. This also determines if the particle encounters
            # a problem boundary, in our case the particle is reflected.
            if surf_cross:
                p.pos, dist2surf, prev_cell = tr.move_part2surf(p, geo, delta_x)
                tr_ln = tr.get_tr_ln(dist2surf, p.dir)
                # Check Right hand boundary
                if p.pos == geo.pos[0] or p.pos == geo.pos[-1]:
                    p.dir = -p.dir
                tally.accumulate(p, prev_cell, tr_ln)
                tally.accumulate_current(p, prev_cell)
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

    # Clear the previous generations flux/fission source to make room for the new flux
    # and fission source
    tally.clear_fission_source()
    tally.clear_flux()

    # Generate the flux and fission source for this generation
    tally.gen_flux(k_tally.num_par, geo)
    tally.gen_fission_source(geo, mat_array)
    tally.gen_mesh_flux(k_tally.num_gen)
    pp.plot_flux(tally.track_length, "Flux", "Cell #", "Flux (1/cm^2)", "Fast Flux", "Thermal Flux")
    pp.plot_1d_array(tally.fission_source, "Fission Source", "Cell #", "Probability", "Fission Source")

    # Now that we have generated our new flux/fission source, erase the tracklength tally
    tally.clear_track_length()
    if i < k_tally.num_gen:
        print(k_tally.k_tally[i])
        new_k = k_tally.get_k(k_tally.k_tally[i], geo, tally.fission_source)
        k_tally.accumulate_k(i+1, new_k)

    tally.clear_current()
    tally.clear_mesh()
    #pp.plot_flux(tally.flux, "Flux", "Cell #", "Flux (1/cm^2)", "Fast Flux", "Thermal Flux")
    #pp.plot_flux(tally.mesh_flux)
    #pp.plot_flux(cell_check)
    if i > 98:
        thermal_flux = pp.pin_cell_average_flux(tally.flux[:, 1])
        fast_flux = pp.pin_cell_average_flux(tally.flux[:, 0])
        pp.plot_flux(thermal_flux)
        pp.plot_flux(fast_flux)
        pp.plot_flux(tally.current[:, :2])
        pp.plot_flux(tally.flux[:, :2])
        pp.plot_flux(tally.fission_source)
        pp.plot_flux(tally.mesh)
        pp.plot_flux(k_tally.k_tally)



k_tally.get_k_final_unc()
print("Final k value of ", k_tally.k_final, " with uncertainty ", k_tally.k_unc)

time1 = time.time()
print('1D MC took: ', time1-time0, 's to run.')