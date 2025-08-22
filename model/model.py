import numpy as np
from .particle import Particle
from .lattice import Lattice

class Model:
	def __init__(self):
		self.particle = Particle(0.4, -0.1)
		self.lattice = Lattice(10, 8, 12)

	def set_particle(self, x, xp, s=0):
		self.particle = Particle(x, xp, s)

	def set_to_last(self):
		self.particle.set_to_last()

	def set_lattice(self, drift_length, focal_length, num_cells, quad_divisions = 5, drift_divisions = 5):
		self.lattice = Lattice(drift_length, focal_length, num_cells, quad_divisions, drift_divisions)

	def get_num_lattice_elements(self):
		return self.lattice.num_cell_elements

	def get_orbit_data(self, coordinate):
		return self.particle.get_orbit_data(coordinate)

	def max_orbit_values(self):
		return self.particle.max_orbit_values()

	def min_orbit_values(self):
		return self.particle.min_orbit_values()

	def propagate(self):
		for _ in range(self.lattice.num_cells):
			for _ in range(self.lattice.quad_divisions):
				next_coordinates = self.lattice.quad_s_vector + self.lattice.fquad_matrix @ self.particle.last
				self.particle.orbit.append(next_coordinates)

			for _ in range(self.lattice.drift_divisions):
				next_coordinates = self.lattice.drift_s_vector + self.lattice.drift_matrix @ self.particle.last
				self.particle.orbit.append(next_coordinates)

			for _ in range(self.lattice.quad_divisions):
				next_coordinates = self.lattice.quad_s_vector + self.lattice.dquad_matrix @ self.particle.last
				self.particle.orbit.append(next_coordinates)

			for _ in range(self.lattice.drift_divisions):
				next_coordinates = self.lattice.drift_s_vector + self.lattice.drift_matrix @ self.particle.last
				self.particle.orbit.append(next_coordinates)
