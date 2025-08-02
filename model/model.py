import numpy as np

class Model:
	def __init__(self):
		pass

	def make_particle(x, xp, s=0):
		return Particle(x, xp, s)

	def make_lattice(drift_length, focal_length, num_cells, quad_divisions = 5, drift_divisions = 5):
		return Lattice(drift_length, focal_length, num_cells, quad_divisions = 5, drift_divisions = 5)

	def propagate(self, particle, lattice):
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
