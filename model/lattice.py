import numpy as np
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
