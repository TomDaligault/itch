import tkinter as tk

from .compound_widgets import *

class SingleParticleView:
	#list of names used to dynamically create tab buttons
	tab_names = ["tab 1", "tab 2", "tab 3"]

	callback_routing_table = {
	'run_animation': 'animation_controls_widget',
	'continue_animation': 'animation_controls_widget',
	'clear': 'animation_controls_widget',
	'randomize_particle': 'particle_controls_widget',
	'on_cell_scale_change': 'cell_element_selector',
	'on_animation_complete': 'plots_widget',
	'on_tab_clicked': 'tabs_widget',
	}

	def __init__(self, parent):
		#list of data to be plotted
		self.static_plot_data = [] 
		self.animated_plot_data = [] 

		self.build_ui(parent)


	def build_ui(self, parent):
		#self contains the user frame (left) and figure frame (right)
		self.user_frame = tk.Frame(parent)
		self.plots_widget = TransversePlotsWidget(parent)
		self.user_frame.pack(side='left', fill='y')
		self.plots_widget.pack(side='right', fill='both', expand=True)

		#user frames is split vertically. Tabs frame on top, control frame underneath. Tabs frame contains tab buttons
		self.tabs_widget = Tabs(self.user_frame, self.tab_names)
		self.control_frame = tk.Frame(self.user_frame)
		self.tabs_widget.pack(side='top', fill='x')
		self.control_frame.pack(side='top')

		# #control frame contains all other user-control frames.
		# #widgets inside these frames must be placed using the grid() method to make their visibility toggleable. 
		self.lattice_controls_widget = LatticeControls(self.control_frame)
		self.particle_controls_widget = ParticleControls(self.control_frame)
		self.animation_controls_widget = AnimationControls(self.control_frame)
		self.cell_element_selector = CellElementSelector(self.control_frame)
		self.lattice_controls_widget.pack(side='top', pady=10)
		self.particle_controls_widget.pack(side='top', pady=10)
		self.animation_controls_widget.pack(side='top', pady=10)
		self.cell_element_selector.pack(side='top', pady=10)

	def set_callback_function(self, callback_name, callback_func):
		widget_name = self.callback_routing_table.get(callback_name)
		if widget_name is None:
			raise KeyError(f'{callback_name} is not mapped to any widgets')
		widget = getattr(self, widget_name)
		widget.set_callback_function(callback_name, callback_func)

	def set_tab_names(self, tab_names):
		self.tabs_widget.set_tab_names(tab_names)

	def set_lattice_inputs(self, drift_length, focal_length, num_cells):		
		self.lattice_controls_widget.set_lattice_inputs(drift_length, focal_length, num_cells)

	def set_particle_inputs(self, x, xp):
		self.particle_controls_widget.set_particle_inputs(x, xp)

	def get_particle_inputs(self):
		return self.particle_controls_widget.get_particle_inputs()

	def get_lattice_inputs(self):
		return self.lattice_controls_widget.get_lattice_inputs()

	def get_animation_speed(self):
		return self.animation_controls_widget.get_speed()

	def get_cell_scale_value(self):
		return self.cell_element_selector.get_scale_value()

	def update_cell_scale(self, scale_length):
		self.cell_element_selector.set_scale_length(scale_length)

	def set_animation_interval(self, interval):
		self.plots_widget.set_animation_interval(interval)

	def disable_animation_controls(self):
		#disable controls that would cause visual artifacts while blitting
		self.animation_controls_widget.disable_widget('run_button')
		self.animation_controls_widget.disable_widget('continue_button')
		self.animation_controls_widget.disable_widget('speed_menu')
		self.cell_element_selector.disable_widget('cell_scale')

	def restore_animation_controls(self):
		self.animation_controls_widget.enable_widget('run_button')
		self.animation_controls_widget.enable_widget('continue_button')
		self.animation_controls_widget.enable_widget('speed_menu')
		self.cell_element_selector.enable_widget('cell_scale')

	#Stop animation, restore UI controls, clear plots. Used when changing tabs, or manually clearing plots.
	def clear_plots(self):
		self.plots_widget.clear_plots()
		self.animation_controls_widget.enable_widget('run_button')
		self.animation_controls_widget.disable_widget('continue_button')
		self.cell_element_selector.disable_widget('cell_scale')

	def relimit_plots(self, x_max, xp_max, s_max, x_min, xp_min, s_min):
		self.plots_widget.relimit_orbit_plot(s_min, s_max, x_min, x_max)
		self.plots_widget.relimit_phase_space_plot(x_min, x_max, xp_min, xp_max) 

	def hide_plot_markers(self):
		self.plots_widget.hide_markers()

	def set_marker_visibility(self, is_visible):
		self.plots_widget.set_marker_visibility(is_visible)

	def display_all_data(self):
		for data in self.static_plot_data:
			self.plots_widget.plot_data(*data)

		for data in self.animated_plot_data:
			self.plots_widget.animate_data(*data)

	def set_static_data(self, x_data, xp_data, s_data):
		self.static_plot_data.append((x_data, xp_data, s_data))

	def set_animated_data(self, x_data, xp_data, s_data):
		self.animated_plot_data.append((x_data, xp_data, s_data))

	def clear_all_data(self):
		self.static_plot_data = []
		self.animated_plot_data = []

	#Used to insure that every widget is visible after changing tabs.
	def restore_default_ui(self):
		for frame in self.control_frame.children.values():
			for widget in frame.children.values():
				widget.grid()
				widget.configure(state='normal')
		self.animation_controls_widget.disable_widget('continue_button')

		self.set_marker_visibility(True)
		self.clear_plots()

	def set_exercise_1(self):
		self.set_marker_visibility(False)
		self.lattice_controls_widget.set_lattice_inputs(10, 8, 1)
		self.particle_controls_widget.set_particle_inputs(0.4, -0.1)

		self.animation_controls_widget.set_speed('slow')
		self.animation_controls_widget.hide_widget('speed_menu')
		self.animation_controls_widget.hide_widget('continue_button')
		self.cell_element_selector.hide_widget('cell_diagram')
		self.cell_element_selector.hide_widget('cell_scale')
		self.lattice_controls_widget.disable_all_widgets()

	def set_exercise_2(self):
		self.set_marker_visibility(False)
		self.lattice_controls_widget.set_lattice_inputs(10, 8, 12)
		self.particle_controls_widget.set_particle_inputs(0.4, -0.1)

		self.animation_controls_widget.set_speed('med')
		self.animation_controls_widget.hide_widget('speed_menu')
		self.animation_controls_widget.hide_widget('continue_button')
		self.cell_element_selector.hide_widget('cell_diagram')
		self.cell_element_selector.hide_widget('cell_scale')
		self.particle_controls_widget.disable_all_widgets()

	def set_exercise_3(self):
		self.lattice_controls_widget.set_lattice_inputs(10, 40, 25)
		self.particle_controls_widget.set_particle_inputs(0.4, -0.1)

		self.animation_controls_widget.set_speed('med')
		self.animation_controls_widget.hide_widget('speed_menu')
		self.animation_controls_widget.hide_widget('continue_button')
		self.cell_element_selector.hide_widget('cell_diagram')
		self.cell_element_selector.hide_widget('cell_scale')
		self.particle_controls_widget.disable_all_widgets()

	def set_exercise_4(self):
		self.lattice_controls_widget.set_lattice_inputs(10, 40, 25)
		self.particle_controls_widget.set_particle_inputs(0.4, -0.1)

		self.animation_controls_widget.set_speed('fast')
		self.animation_controls_widget.hide_widget('speed_menu')
		self.animation_controls_widget.hide_widget('continue_button')
		self.lattice_controls_widget.disable_all_widgets()

	def set_undefined_exercise(self):
		self.lattice_controls_widget.set_lattice_inputs(10, 40, 30)
		self.particle_controls_widget.set_particle_inputs(0.4, -0.1)

		self.animation_controls_widget.set_speed('fast')
