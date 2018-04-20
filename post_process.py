import numpy as np
import matplotlib.pyplot as mpl

def plot_flux(flux, title, x_label, y_label, label_1, label_2):
    mpl.plot(flux[:,0], label=label_1)
    mpl.plot(flux[:,1], label=label_2)
    mpl.legend()
    mpl.title(title)
    mpl.xlabel(x_label)
    mpl.ylabel(y_label)
    mpl.show()

def plot_1d_array(flux, title, x_label, y_label, label_1):
    mpl.plot(flux[:], label=label_1)
    mpl.legend()
    mpl.title(title)
    mpl.xlabel(x_label)
    mpl.ylabel(y_label)
    mpl.show()

def pin_cell_average_flux(flux):
    pin_cell = np.reshape(flux,(16,3))
    pin_cell_avg = np.zeros(16)
    for i, x in enumerate(pin_cell):
        pin_cell_avg[i] = sum(x)
    return pin_cell_avg