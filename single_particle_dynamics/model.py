import numpy as np
import time

class Particle():
	def __init__(self, x, xp, s=0):
		self.orbit = [np.array([[x], [xp], [s]], dtype=float)]

	@property
	def last(self):
		return self.orbit[-1] #Last element in the orbit list.

	def get_orbit(self):
		orbit = np.array(self.orbit)
		orbit = np.stack(orbit)
		return orbit

	def get_orbit_data(self, coordinate):
		orbit = self.get_orbit()
		coordinate_index = {'x': 0, 'xp': 1, 's': 2}
		if coordinate in coordinate_index:
			return orbit[:, coordinate_index[f'{coordinate}'], 0]

		else:
			raise ValueError(f"Coordinate must be x, xp, or s")
		
	def max_values(self):
		orbit = self.get_orbit()
		x_max = orbit[:,0,0].max()
		xp_max = orbit[:,1,0].max()
		s_max = orbit[:,2,0].max()

		return x_max, xp_max, s_max

	def min_values(self):
		orbit = self.get_orbit()
		x_min = orbit[:,0,0].min()
		xp_min = orbit[:,1,0].min()
		s_min = orbit[:,2,0].min()

		return x_min, xp_min, s_min

	def set_to_last(self):
		self.orbit = [self.last]

'''Defines transfer matrices from give lattice parameters.'''
'''Supports optionally subdividing lattice elements via quad_divisions and drift_divisions. Default is 5 subdivisions.'''
class Lattice:
	def __init__(self, drift_length, focal_length, num_cells, quad_divisions = 5, drift_divisions = 5):
		self.focal_length = focal_length
		self.drift_length = drift_length
		self.num_cells = num_cells

		self.quad_divisions = quad_divisions
		self.drift_divisions = drift_divisions
		self.num_cell_elements = 2*(drift_divisions + quad_divisions)

		self.fquad_matrix = np.array([[1, 0, 0], 
									  [(-1/ (focal_length * quad_divisions)), 1, 0], 
									  [0, 0, 1]])

		self.dquad_matrix = np.array([[1, 0, 0], 
									  [(1/(focal_length * quad_divisions)), 1, 0],
									  [0, 0, 1]])

		self.drift_matrix = np.array([[1, (drift_length / drift_divisions), 0],
									 [0, 1, 0], 
									 [0, 0, 1]])

		self.quad_s_vector = np.array([[0],
									   [0],
									   [0]])

		self.drift_s_vector = np.array([[0],
										[0],
										[drift_length / drift_divisions]])

def propagate(particle, lattice):
		for _ in range(lattice.num_cells):
			for _ in range(lattice.quad_divisions):
				next_coordinates = lattice.quad_s_vector + lattice.fquad_matrix @ particle.last
				particle.orbit.append(next_coordinates)

			for _ in range(lattice.drift_divisions):
				next_coordinates = lattice.drift_s_vector + lattice.drift_matrix @ particle.last
				particle.orbit.append(next_coordinates)

			for _ in range(lattice.quad_divisions):
				next_coordinates = lattice.quad_s_vector + lattice.dquad_matrix @ particle.last
				particle.orbit.append(next_coordinates)

			for _ in range(lattice.drift_divisions):
				next_coordinates = lattice.drift_s_vector + lattice.drift_matrix @ particle.last
				particle.orbit.append(next_coordinates)


if __name__ == '__main__':



	particle = Particle(0.4, -0.1)
	lattice = Lattice(10, 8, 12, quad_divisions=1, drift_divisions=1)

	propagate(particle, lattice)

	print(particle.last)