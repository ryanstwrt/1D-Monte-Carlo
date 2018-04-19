import numpy as np
import matplotlib.pyplot as mpl

def plot_flux(flux):
    mpl.plot(flux)
    mpl.show()

def pin_cell_average_flux(flux):
    pin_cell = np.reshape(flux,(16,3))
    pin_cell_avg = np.zeros(16)
    for i, x in enumerate(pin_cell):
        pin_cell_avg[i] = sum(x)
    return pin_cell_avg