import numpy as np
from .particle import Particle
from .lattice import Lattice

class Model:
	def __init__(self):
		self.lattice = None

		self.active_particle = None
		self.active_orbit = []

		self.particles = []

	def clear_particles(self):
		self.particles = []
		self.active_particle = None

	def set_lattice(self, drift_length, focal_length, num_cells, quad_divisions=5, drift_divisions=5):
		self.lattice = Lattice(drift_length, focal_length, num_cells, quad_divisions, drift_divisions)

	def get_num_lattice_elements(self):
		return self.lattice.num_cell_elements

	#Make a new particle, add it to self.particles, set it as the active particle
	def make_new_particle(self, x, xp, s=0):
		new_particle = Particle(x, xp, s)
		self.particles.append(new_particle)
		self.set_active_particle(-1)

	#Take particle at index, set it as the active particle. 
	def stage_particle(self, index):
		self.set_active_particle(index)
		self.active_orbit = self.particles[index]

	def set_active_particle(self, index):
		self.active_particle = self.particles[index]

	def propagate_active_particle(self):
		if self.active_particle is None:
			raise AttributeError(f"Active particle is not set")
		if self.lattice is None:
			raise AttributeError(f"Lattice is not set")

		self.active_orbit = self.calculate_orbit(self.active_particle, self.lattice)


	def get_active_orbit_data(self):
		# massage the orbit into a 3xn numpy array where n is the number on elements in self.orbit. Rows map to coordinate_index
		return np.hstack(self.active_orbit)

	def get_previous_orbits(self):
		return [particle.get_orbit_data() for particle in self.particles]

	def commit_active_orbit(self):
		self.active_orbit.pop(0) #calculate_orbit causes a double-count between the first element of active_orbit and the last element of particle.orbit
		self.active_particle.commit_to_orbit(self.active_orbit)

		self.active_orbit = None

	def calculate_orbit(self, particle, lattice):
		current_orbit = [particle.orbit[-1]] #Grab the most recent coordinates for the particle.

		for _ in range(lattice.num_cells):
			for _ in range(lattice.quad_divisions):
				next_coordinates = lattice.quad_s_vector + lattice.fquad_matrix @ current_orbit[-1]
				current_orbit.append(next_coordinates)

			for _ in range(lattice.drift_divisions):
				next_coordinates = lattice.drift_s_vector + lattice.drift_matrix @ current_orbit[-1]
				current_orbit.append(next_coordinates)

			for _ in range(lattice.quad_divisions):
				next_coordinates = lattice.quad_s_vector + lattice.dquad_matrix @ current_orbit[-1]
				current_orbit.append(next_coordinates)

			for _ in range(lattice.drift_divisions):
				next_coordinates = lattice.drift_s_vector + lattice.drift_matrix @ current_orbit[-1]
				current_orbit.append(next_coordinates)

		return current_orbit

	def max_orbit_values(self):
	    all_orbits = [self.get_active_orbit_data()] + [particle.get_orbit_data() for particle in self.particles]
	    current_orbit = np.hstack(all_orbits)
	    return np.max(current_orbit, axis=1)

	def min_orbit_values(self):
	    all_orbits = [self.get_active_orbit_data()] + [particle.get_orbit_data() for particle in self.particles]
	    current_orbit = np.hstack(all_orbits)
	    return np.min(current_orbit, axis=1)