import utils as ut
import numpy as np

# Creates a class for the particle which contains the particles weight,
# position, cell, energy (where energy 0 is fast), and direction
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
        self.enrg = 0
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

mesh = flux = np.arange(0, 4)
print(mesh)

p = gen_particle(1.0, 0, mesh, flux)
print(p.wt, p.pos, p.cell, p.enrg, p.dir)