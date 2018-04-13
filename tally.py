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


def init_k_tally(kcode):
    k = k_code_tally()
    k.num_par(kcode)
    k.num_gen(kcode)
    k.num_skip_gen(kcode)
    k.init_k(kcode)

    k_tally_vector = np.zeros(int(k.num_gen - k.num_skip_gen))

init_k_tally(su.k_code)
