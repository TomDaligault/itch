import numpy as np
import tkinter as tk

class Presenter:
	def __init__(self, view, model):
		self.view = view
		self.model = model
		#Passed to the view to dynamically create tab buttons
		self.tab_names = ['exercise 1', 'exercise 2', 'exercise 3', 'exercise 4', ' ']
		#Dictionary of callback functions. Used to set the view's callback registry.
		self.callback_registry = {'run_animation': [self.start_animation],
							 'continue_animation': [self.continue_animation],
							 'on_tab_clicked': [self.change_tab], 
							 'on_cell_scale_change': [self.update_plot_markers],
							 'randomize_particle': [self.randomize_particle],
							 'clear': [self.clear_plots]}

		#Sets the number of subdivisions of lattice elements. More divisions means smoother animations but more frames.
		self.cell_divisions = {'drift_divisions': 5, 'quad_divisions': 5}
		self.view.set_callback_registry(self.callback_registry)
		self.view.set_tab_names(self.tab_names)
		self.view.build_ui()

#Restores default, then set exercises based on the name of the tab that was clicked.
	def change_tab(self, tab_name):
		self.view.restore_default_ui()
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

	def start_animation(self):
		self._run_animation(continue_run=False)

	def continue_animation(self):
		self._run_animation(continue_run=True)

	def _run_animation(self, continue_run=False):
		self.view.disable_animation_controls()

		if not continue_run:
			self.update_particle()
		else:
			self.model.set_to_last()

		self.update_lattice()
		self.model.propagate()
		self.update_plot_markers()
		self.relimit_plots()
		self.update_animation_interval()

		x_data = self.model.get_orbit_data('x')
		xp_data = self.model.get_orbit_data('xp')
		s_data = self.model.get_orbit_data('s')

		self.view.plots_widget.animate_plots(x_data, xp_data, s_data, callback=self.view.restore_animation_controls)
		
	def update_particle(self):
		x, xp = self.view.get_particle_inputs()
		self.model.set_particle(x, xp)

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
		self.view.plots_widget.set_markers(marker_start=scale_value, marker_spacing=num_lattice_elements)

	def relimit_plots(self):
		x_max, xp_max, s_max = self.model.max_orbit_values()
		x_min, xp_min, s_min = self.model.min_orbit_values()
		self.view.relimit_plots(x_max, xp_max, s_max, x_min, xp_min, s_min)

	def clear_plots(self):
		self.view.clear_plots()
		self.view.animation_controls_widget.enable_widget('run_button')
		self.view.animation_controls_widget.disable_widget('continue_button')
		self.view.cell_element_selector.disable_widget('cell_scale')