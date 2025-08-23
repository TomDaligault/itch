import numpy as np

def make_single_particle(x, xp, s=0):
	return np.array([[x], [xp], [s]], dtype=float)
