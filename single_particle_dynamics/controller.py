import numpy as np

import tkinter as tk
from numpy import random
from view import View
import model

class Controller:
	def __init__(self, view):
		self.view = view
		#Passed to the view to dynamically create tab buttons
		self.tab_names = ['exercise 1', 'exercise 2', 'exercise 3', 'exercise 4', 'sandbox']
		#Dictionary of callback functions. Used to set the view's callback registry.
		self.callback_registry = {'run_animation': [self.run_animation],
							 'continue_animation': [self.continue_animation],
							 'on_tab_change': [self.change_tab],
							 'on_cell_scale_change': [self.update_ellipse],
							 'randomize_particle': [self.randomize_particle],
							 'clear_plots': [self.clear_plots]}

		self.particle = model.Particle(0.4, -0.1)

		#Sets the number of subdivisions of lattice elements. More divisions means smoother animations but more frames.
		self.cell_divisions = {'drift_divisions': 5, 'quad_divisions': 5}
		self.lattice = model.Lattice(10, 8, 12, **self.cell_divisions)


	def main(self):
		self.view.callback_registry = self.callback_registry
		self.view.tab_names = self.tab_names
		self.view.main()

	def randomize_particle(self):
		self.view.set_particle_inputs(round(random.normal(),2), round(random.normal(),2))

	def change_tab(self, tab_name):
		self.view.restore_default_control_frame() #Insure that all controls are visible after changing tabs.
		self.view.clear_plots()

		#Set visibility of plot markers, modify UI for specific exercises.
		if tab_name == 'exercise 1':
			self.view.plots_frame.hide_markers()
			self.view.set_exercise_1()
		elif tab_name == 'exercise 2':
			self.view.plots_frame.hide_markers()
			self.view.set_exercise_2()
		elif tab_name == 'exercise 3':
			self.view.plots_frame.show_markers()
			self.view.set_exercise_3()
		elif tab_name == 'exercise 4':
			self.view.plots_frame.show_markers()
			self.view.set_exercise_4()
		else:
			self.view.animation_control_frame.continue_button.configure(state='disabled')
			self.view.plots_frame.show_markers()

	def update_particle(self):
		x, xp = self.view.get_particle_inputs()
		self.particle = model.Particle(x, xp)
		
	def update_lattice(self):
		drift_length, focal_length, num_cells = self.view.get_lattice_inputs()
		self.lattice = model.Lattice(drift_length, focal_length, num_cells, **self.cell_divisions)

	#This method is used as a callback when updating the cell_scale.
	def update_ellipse(self):
		self.view.update_cell_scale(scale_length = self.lattice.num_cell_elements)
		scale_value = self.view.get_cell_scale_value()
		self.view.plots_frame.set_markers(marker_start=scale_value, marker_spacing=self.lattice.num_cell_elements)

	def run_animation(self):
		self.view.disable_animation_controls()

		self.update_particle()
		self.update_lattice()
		model.propagate(self.particle, self.lattice)
		self.update_ellipse()
		self.relimit_plots()

		x_data = self.particle.get_orbit_data('x')
		xp_data = self.particle.get_orbit_data('xp')
		s_data = self.particle.get_orbit_data('s')

		interval = self.view.get_animation_speed()
		self.view.plots_frame.set_animation_interval(interval)
		self.view.plots_frame.animate_plots(x_data, xp_data, s_data, callback=self.view.restore_animation_controls)

	def continue_animation(self):
		self.view.disable_animation_controls()

		self.particle.set_to_last()
		self.update_lattice()
		model.propagate(self.particle, self.lattice)
		self.update_ellipse()
		self.relimit_plots()

		x_data = self.particle.get_orbit_data('x')
		xp_data = self.particle.get_orbit_data('xp')
		s_data = self.particle.get_orbit_data('s')

		interval = self.view.get_animation_speed()
		self.view.plots_frame.set_animation_interval(interval)
		self.view.plots_frame.animate_plots(x_data, xp_data, s_data, callback=self.view.restore_animation_controls)

	def relimit_plots(self):
		x_max, xp_max, s_max = self.particle.max_values()
		x_min, xp_min, s_min = self.particle.min_values()
		self.view.relimit_plots(x_max, xp_max, s_max, x_min, xp_min, s_min)

	def clear_plots(self):
		self.view.clear_plots()
		self.view.animation_control_frame.continue_button.configure(state='disabled')
		


if __name__ == '__main__':
	view = View()
	controller = Controller(view)
	controller.main()