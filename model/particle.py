import numpy as np

class Particle():
	def __init__(self, x, xp, s=0):
		#self.orbit is a list of 3x1 numpy arrays
		self.orbit = [np.array([[x], [xp], [s]], dtype=float)]

	def set_orbit(self, new_orbit):
		self.orbit = new_orbit

	def set_to_last(self):
		self.set_orbit([self.orbit[-1]]) #set self.orbit to a new list containing only the last element of old self.orbit

	def get_orbit_data(self, coordinate):
		coordinate_index = {'x': 0, 'xp': 1, 's': 2}

		#massage the orbit into an nx3 numpy array where n is the number on elements in self.orbit. Rows map to coordinate_index
		orbit = np.array(self.orbit)
		orbit = np.stack(orbit)
		orbit = np.squeeze(orbit, axis=-1)

		if coordinate in coordinate_index:
			return orbit[:, coordinate_index[f'{coordinate}']]
		else:
			raise ValueError(f"Coordinate must be x, xp, or s")
		
	def max_orbit_values(self):
		x_max = self.get_orbit_data('x').max()
		xp_max = self.get_orbit_data('xp').max()
		s_max = self.get_orbit_data('s').max()
		return x_max, xp_max, s_max

	def min_orbit_values(self):
		x_min = self.get_orbit_data('x').min()
		xp_min = self.get_orbit_data('xp').min()
		s_min = self.get_orbit_data('s').min()
		return x_min, xp_min, s_min