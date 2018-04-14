import set_up as su
import numpy as np


class k_code_tally:
    def num_par(self, kcode):
        self.num_par = kcode[0]

    def num_gen(self, kcode):
        self.num_gen = kcode[1]

    def num_skip_gen(self, kcode):
        self.num_skip_gen = kcode[2]

    def init_k(self, kcode):
        self.init_k = kcode[3]

    def k_tally(self, k):
        self.k_tally = np.zeros(int(k.num_gen - k.num_skip_gen))


def init_k_tally(kcode):
    k = k_code_tally()
    k.num_par(kcode)
    k.num_gen(kcode)
    k.num_skip_gen(kcode)
    k.init_k(kcode)
    k.k_tally(k)
    return k


# Right now it just takes in a dummy cell
# needs to be converted to p.cell
class mesh_tally():
    def init_mesh(self, mesh):
        self.mesh = np.zeros(mesh)

    def accumulate(self, mesh, p_cell, tr_len):
        for i, x in enumerate(mesh):
            if i == p_cell:
                mesh[i] += tr_len
                break

def init_mesh_tally(geo):
    mt = mesh_tally()
    mt.init_mesh(len(geo.mesh))
    return mt

#mesh_tal = init_mesh_tally(su.geo)
#k = init_k_tally(su.k_code)

#for x in range(len(mesh_tal.mesh)):
#    cell = 41
#    tr_len = x + 1
#    mesh_tal.accumulate(mesh_tal.mesh, cell, tr_len)
#print(mesh_tal.mesh)