import numpy as np
import tkinter as tk

class Presenter:
	def __init__(self, view, model):
		self.view = view
		self.model = model
		#Passed to the view to dynamically create tab buttons
		self.tab_names = ['exercise 1', 'exercise 2', 'exercise 3', 'exercise 4', ' ']

		#Sets the number of subdivisions of lattice elements. More divisions means smoother animations but more frames.
		self.cell_divisions = {'drift_divisions': 5, 'quad_divisions': 5}

		self.view.set_tab_names(self.tab_names)
		self.tab_names.pop(1)
		self.view.set_tab_names(self.tab_names)

		self.view.set_callback_function('run_animation', lambda: self.start_animation(continue_run=False))
		self.view.set_callback_function('continue_animation', lambda: self.start_animation(continue_run=True))
		self.view.set_callback_function('on_animation_complete', self.on_animation_complete)
		self.view.set_callback_function('clear', self.clear_plots)
		self.view.set_callback_function('randomize_particle', self.randomize_particle)
		self.view.set_callback_function('on_cell_scale_change', self.update_plot_markers)
		self.view.set_callback_function('on_tab_clicked', self.change_tab)


#Restores default, then set exercises based on the name of the tab that was clicked.
	def change_tab(self, tab_name):
		self.view.restore_default_ui()
		self.view.clear_all_data()
		self.model.clear_particles()

		if tab_name == 'exercise 1':
			self.view.set_exercise_1()
		elif tab_name == 'exercise 2':
			self.view.set_exercise_2()
		elif tab_name == 'exercise 3':
			self.view.set_exercise_3()
		elif tab_name == 'exercise 4':
			self.view.set_exercise_4()
		else:
			self.view.set_undefined_exercise()

	def start_animation(self, continue_run=False):
		self.view.disable_animation_controls()
		self.view.clear_plots()

		if not continue_run:
			self.update_particle()
		else:
			self.model.stage_particle(-1)

		self.update_lattice()
		self.model.propagate_active_particle()
		self.update_plot_markers()
		self.relimit_plots()
		self.update_animation_interval()

		previous_orbits = self.model.get_previous_orbits()
		for orbit in previous_orbits:
			self.view.set_static_data(orbit[0], orbit[1], orbit[2])

		x_data, xp_data, s_data = self.model.get_active_orbit_data()
		self.view.set_animated_data(x_data, xp_data, s_data)
		self.view.display_all_data()

		self.model.commit_active_orbit()
		self.view.clear_all_data()

	def on_animation_complete(self):
		self.view.restore_animation_controls()
		
	def update_particle(self):
		x, xp = self.view.get_particle_inputs()
		self.model.make_new_particle(x, xp)

	def randomize_particle(self):
		self.view.set_particle_inputs(round(np.random.normal(),2), round(np.random.normal(),2))
		
	def update_lattice(self):
		drift_length, focal_length, num_cells = self.view.get_lattice_inputs()
		self.model.set_lattice(drift_length, focal_length, num_cells, **self.cell_divisions)

	def update_animation_interval(self):
		interval = self.view.get_animation_speed()
		self.view.set_animation_interval(interval)

	#This method is used as a callback when updating the cell_scale.
	def update_plot_markers(self):
		num_lattice_elements = self.model.get_num_lattice_elements()
		self.view.update_cell_scale(scale_length=num_lattice_elements)

		scale_value = self.view.get_cell_scale_value()
		self.view.plots_widget.set_markers(marker_start=scale_value)

	def relimit_plots(self):
		x_max, xp_max, s_max = self.model.max_orbit_values()
		x_min, xp_min, s_min = self.model.min_orbit_values()
		self.view.relimit_plots(x_max, xp_max, s_max, x_min, xp_min, s_min)

	def clear_plots(self):
		self.model.clear_particles()
		self.view.clear_plots()