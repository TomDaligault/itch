import numpy as np
from .particle import make_single_particle
from .lattice import Lattice

class Model:
	def __init__(self):
		self.particle = make_single_particle(0.4, -0.1)
		self.lattice = Lattice(10, 8, 12)
		self.orbit = [self.particle]

	def set_particle(self, x, xp):
		self.particle = make_single_particle(x, xp)
		self.orbit = [self.particle]

	def set_lattice(self, drift_length, focal_length, num_cells, quad_divisions = 5, drift_divisions = 5):
		self.lattice = Lattice(drift_length, focal_length, num_cells, quad_divisions, drift_divisions)

	def get_num_lattice_elements(self):
		return self.lattice.num_cell_elements

	def set_to_last(self):
		self.orbit = [self.orbit[-1]]

	def propagate(self):
		for _ in range(self.lattice.num_cells):
			for _ in range(self.lattice.quad_divisions):
				next_coordinates = self.lattice.quad_s_vector + self.lattice.fquad_matrix @ self.orbit[-1]
				self.orbit.append(next_coordinates)

			for _ in range(self.lattice.drift_divisions):
				next_coordinates = self.lattice.drift_s_vector + self.lattice.drift_matrix @ self.orbit[-1]
				self.orbit.append(next_coordinates)

			for _ in range(self.lattice.quad_divisions):
				next_coordinates = self.lattice.quad_s_vector + self.lattice.dquad_matrix @ self.orbit[-1]
				self.orbit.append(next_coordinates)

			for _ in range(self.lattice.drift_divisions):
				next_coordinates = self.lattice.drift_s_vector + self.lattice.drift_matrix @ self.orbit[-1]
				self.orbit.append(next_coordinates)

	def get_orbit_data(self, coordinate):
		orbit = np.array(self.orbit)
		orbit = np.stack(orbit)
		orbit = np.squeeze(orbit, axis=-1)

		coordinate_index = {'x': 0, 'xp': 1, 's': 2}

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
