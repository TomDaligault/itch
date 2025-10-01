import numpy as np

class Particle():
	def __init__(self, x, xp, s=0):
		#self.orbit is a list of 3x1 numpy arrays
		self.orbit = [np.array([[x], [xp], [s]], dtype=float)]

	def commit_to_orbit(self, new_orbit):
		self.orbit += new_orbit

	def get_last_value(self):
		return self.orbit[-1]

	def get_orbit_data(self):
		# massage the orbit into a 3xn numpy array where n is the number on elements in self.orbit. Rows are x, xp, s respectively
		return np.hstack(self.orbit)