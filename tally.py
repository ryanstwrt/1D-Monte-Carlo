import numpy as np
import set_up

class k_code_tally:
    def num_par(self, kcode):
        self.num_par = int(kcode[0])

    def num_gen(self, kcode):
        self.num_gen = int(kcode[1])

    def num_skip_gen(self, kcode):
        self.num_skip_gen = int(kcode[2])

    def init_k(self, kcode):
        self.init_k = kcode[3]

    def k_tally(self, k):
        self.k_tally = np.zeros(k.num_gen+1)
        self.k_tally[0] = 1.0

    def accumulate_k(self, i, k):
        self.k_tally[i] = k

    def get_k(self, k, geo, fission_source):
        new_k = 0
        for i, fs in enumerate(fission_source):
            new_k += fs * (geo.pos[i+1]-geo.pos[i])
        new_k = k * new_k
        return new_k

    def get_k_final_unc(self):
        varience = self.k_tally[self.num_skip_gen:] ** 2
        tracked_gen = (self.num_gen - self.num_skip_gen)
        print(varience)
        varience_scaler = np.sum(varience)
        print(varience_scaler)
        #self.k_unc = np.sqrt(varience_scaler) * (tracked_gen-1) * (tracked_gen)
        self.k_final = sum(self.k_tally[self.num_skip_gen:]) / tracked_gen
        self.k_unc = (1/((tracked_gen-1) * tracked_gen)) * np.sum((self.k_tally[self.num_skip_gen:] - self.k_final)**2)
        print(self.k_unc)

# Right now it just takes in a dummy cell
class tally():
    def init_track_length(self, mesh):
        self.track_length = np.zeros((mesh, 2))

    def init_flux(self, mesh):
        self.flux = np.zeros((mesh, 4))

    def init_fission_source(self, mesh):
        self.fission_source = np.zeros(mesh)

    def init_current(self, mesh):
        self.current = np.zeros((mesh, 4))

    def init_mesh(self):
        self.mesh = np.zeros((128, 2))

    def init_mesh_flux(self):
        self.mesh_flux = np.zeros((128, 2))

    def accumulate(self, p, prev_cell, tr_len):
        if p.enrg == 1:
            self.track_length[prev_cell][0] += p.wt * tr_len
        else:
            self.track_length[prev_cell][1] += p.wt * tr_len

    def gen_flux(self, num_part, geo):
        for x in geo.cells:
            for i, y in enumerate(self.track_length[x]):
                self.flux[x, i] = y / (num_part * (geo.pos[x+1] - geo.pos[x]))
                self.flux[x, i+2] = (y / (num_part * (geo.pos[x+1] - geo.pos[x]))) ** 2




    def gen_fission_source(self, geo, mat_array):
        xc = set_up.get_XC(1, 0, mat_array)
        for i, y in enumerate(geo.mat):
            x = int(y)
            xc.get_nu(1, x, mat_array)
            nu_f = xc.nu
            xc.get_nu(2, x, mat_array)
            nu_t = xc.nu
            xc.get_fiss_xc(1, x, mat_array)
            fiss_f = xc.fiss_xc
            xc.get_fiss_xc(2, x, mat_array)
            fiss_t = xc.fiss_xc
            self.fission_source[i] = nu_f * fiss_f * self.flux[i, 0] + nu_t * fiss_t * self.flux[i, 1]

    def accumulate_current(self, p, prev_cell):
        cur_enrg = p.enrg -1
        if p.cell > prev_cell:
            self.current[p.cell][cur_enrg] += p.wt
        else:
            self.current[prev_cell][cur_enrg] -= p.wt
        if p.cell > prev_cell:
            self.current[p.cell][cur_enrg+2] += p.wt ** 2
        else:
            self.current[p.cell][cur_enrg+2] -= p.wt ** 2

    def accumulate_mesh(self, p, tl):
        cur_enrg = p.enrg -1
        delta_x = 0.15625
        mesh_pos = 0
        for i, x in enumerate(self.mesh):
            if mesh_pos < p.pos <= (mesh_pos + delta_x):
                self.mesh[i][cur_enrg] += p.wt * tl
                break
            mesh_pos += delta_x

    def gen_mesh_flux(self, num_part):
        for i, y in enumerate(self.mesh):
            self.mesh_flux[i, 0] = y[0] / (num_part * 0.15625)
            self.mesh_flux[i, 1] = y[1] / (num_part * 0.15625)



    def clear_fission_source(self):
        self.fission_source[:] = 0

    def clear_flux(self):
        self.flux[:] = 0

    def clear_track_length(self):
        self.track_length[:] = 0

    def clear_current(self):
        self.current[:] = 0

    def clear_mesh (self):
        self.mesh[:] = 0


def init_k_tally(kcode):
    k = k_code_tally()
    k.num_par(kcode)
    k.num_gen(kcode)
    k.num_skip_gen(kcode)
    k.init_k(kcode)
    k.k_tally(k)
    return k


def init_track_length_tally(geo):
    mt = tally()
    mt.init_track_length(len(geo.cells))
    mt.init_mesh()
    mt.init_mesh_flux()
    mt.init_current(len(geo.cells))
    mt.init_flux(len(geo.cells))
    mt.init_fission_source(len(geo.cells))
    return mt

