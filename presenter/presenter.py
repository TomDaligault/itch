import numpy as np

import tkinter as tk
from numpy import random
from model.particle import Particle
from model.lattice import Lattice

class Presenter:
	def __init__(self, ui, model):
		self.ui = ui
		self.model = model
		#Passed to the ui to dynamically create tab buttons
		self.tab_names = ['exercise 1', 'exercise 2', 'exercise 3', 'exercise 4', ' ']
		#Dictionary of callback functions. Used to set the ui's callback registry.
		self.callback_registry = {'run_animation': [self.run_animation],
							 'continue_animation': [self.continue_animation],
							 'on_tab_clicked': [self.change_tab], 
							 'on_cell_scale_change': [self.update_plot_markers],
							 'randomize_particle': [self.randomize_particle],
							 'clear': [self.clear_plots]}

		#Sets the number of subdivisions of lattice elements. More divisions means smoother animations but more frames.
		self.cell_divisions = {'drift_divisions': 6, 'quad_divisions': 6}
		self.lattice = Lattice(10, 8, 12, **self.cell_divisions)
		self.particle = Particle(0.4, -0.1)

		self.ui.callback_registry = self.callback_registry
		self.ui.tab_names = self.tab_names
		self.ui.build_ui()

	def randomize_particle(self):
		self.ui.set_particle_inputs(round(random.normal(),2), round(random.normal(),2))

#Restores default, then set exercises based on the name of the tab that was clicked.
	def change_tab(self, tab_name):
		self.ui.restore_default_controls()
		if tab_name == 'exercise 1':
			self.ui.set_exercise_1()
		elif tab_name == 'exercise 2':
			self.ui.set_exercise_2()
		elif tab_name == 'exercise 3':
			self.ui.set_exercise_3()
		elif tab_name == 'exercise 4':
			self.ui.set_exercise_4()
		else:
			self.ui.set_undefined_exercise()

	def update_particle(self):
		x, xp = self.ui.get_particle_inputs()
		self.particle = Particle(x, xp)
		
	def update_lattice(self):
		drift_length, focal_length, num_cells = self.ui.get_lattice_inputs()
		self.lattice = Lattice(drift_length, focal_length, num_cells, **self.cell_divisions)

	#This method is used as a callback when updating the cell_scale.
	def update_plot_markers(self):
		self.ui.update_cell_scale(scale_length = self.lattice.num_cell_elements)
		scale_value = self.ui.get_cell_scale_value()
		self.ui.plots_widget.set_markers(marker_start=scale_value, marker_spacing=self.lattice.num_cell_elements)

	def run_animation(self):
		self.ui.disable_animation_controls()

		self.update_particle()
		self.update_lattice()
		self.model.propagate(self.particle, self.lattice)
		self.update_plot_markers()
		self.relimit_plots()

		x_data = self.particle.get_orbit_data('x')
		xp_data = self.particle.get_orbit_data('xp')
		s_data = self.particle.get_orbit_data('s')

		interval = self.ui.get_animation_speed()
		self.ui.plots_widget.set_animation_interval(interval)
		self.ui.plots_widget.animate_plots(x_data, xp_data, s_data, callback=self.ui.restore_animation_controls)

	def continue_animation(self):
		self.ui.disable_animation_controls()

		self.particle.set_to_last()
		self.update_lattice()
		self.model.propagate(self.particle, self.lattice)
		self.update_plot_markers()
		self.relimit_plots()

		x_data = self.particle.get_orbit_data('x')
		xp_data = self.particle.get_orbit_data('xp')
		s_data = self.particle.get_orbit_data('s')

		interval = self.ui.get_animation_speed()
		self.ui.plots_widget.set_animation_interval(interval)
		self.ui.plots_widget.animate_plots(x_data, xp_data, s_data, callback=self.ui.restore_animation_controls)
		
	def relimit_plots(self):
		x_max, xp_max, s_max = self.particle.max_orbit_values()
		x_min, xp_min, s_min = self.particle.min_orbit_values()
		self.ui.relimit_plots(x_max, xp_max, s_max, x_min, xp_min, s_min)

	def clear_plots(self):
		self.ui.clear_plots()
		self.ui.animation_controls_widget.disable_widget('continue_button')