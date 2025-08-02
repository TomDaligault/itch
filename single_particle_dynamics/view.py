import tkinter as tk
from numpy import random

import CustomWidgets
import CompoundWidgets

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class View(tk.Tk):
	def __init__(self, callback_registry=None):
		super().__init__()
		self.title('Single Particle Dynamics')

		#Registry of callback functions. Passed as a kwarg when creating custom widgets
		self.callback_registry = callback_registry or {}

		#list of names used to dynamically create tab buttons
		self.tab_names = ["exercise 1", "exercise 2", "exercise 3", 'exercise 4', ' ']
		#dictionary of tab button and their names, populated dynamically as buttons are created.
		self.tab_buttons = {}

	def main(self):
		#self contains the user frame (left) and figure frame (right)
		self.user_frame = tk.Frame(self)
		self.plots_frame = CompoundWidgets.TransversePlotsWidget(self)
		self.user_frame.pack(side='left', fill='y')
		self.plots_frame.pack(side='right', fill='both', expand=True)

		#user frames is split vertically. Tabs frame on top, control frame underneath. Tabs frame contains tab buttons
		self.tabs_frame = CompoundWidgets.TabsFrame(self.user_frame, self.tab_names, callback_registry=self.callback_registry)
		self.control_frame = tk.Frame(self.user_frame)
		self.tabs_frame.pack(side='top', fill='x')
		self.control_frame.pack(side='top')

		# #control frame contains all other user-control frames.
		# #widgets inside these frames must be placed using the grid() method to make their visibility toggleable. 
		self.lattice_frame = CompoundWidgets.LatticeControlFrame(self.control_frame)
		self.particle_control_frame = CompoundWidgets.ParticleControlFrame(self.control_frame, callback_registry=self.callback_registry)
		self.animation_control_frame = CompoundWidgets.AnimationControlFrame(self.control_frame, callback_registry=self.callback_registry)
		self.cell_diagram_frame = CompoundWidgets.LatticeDiagramFrame(self.control_frame, callback_registry=self.callback_registry)
		self.lattice_frame.pack(side='top', pady=10)
		self.particle_control_frame.pack(side='top', pady=10)
		self.animation_control_frame.pack(side='top', pady=10)
		self.cell_diagram_frame.pack(side='top', pady=10)

		self.mainloop()

	def set_lattice_inputs(self, drift_length, focal_length, num_cells):		
		self.lattice_frame.set_lattice_inputs(drift_length, focal_length, num_cells)

	def set_particle_inputs(self, x, xp):
		self.particle_control_frame.set_particle_inputs(x, xp)

	def get_particle_inputs(self):
		return self.particle_control_frame.get_particle_inputs()

	def get_lattice_inputs(self):
		return self.lattice_frame.get_lattice_inputs()

	def get_animation_speed(self):
		return self.animation_control_frame.anim_speed_option.get_speed()

	def get_cell_scale_value(self):
		return self.cell_diagram_frame.cell_scale.get()

	def update_cell_scale(self, scale_length):
		self.cell_diagram_frame.cell_scale.configure(to=scale_length)

	def disable_animation_controls(self):
		#disable controls that would cause visual artifacts while blitting
		self.animation_control_frame.run_button.configure(state = 'disabled')
		self.animation_control_frame.continue_button.config(state = 'disabled')
		self.animation_control_frame.anim_speed_option.configure(state ='disabled')
		self.cell_diagram_frame.cell_scale.configure(state = 'disabled')

	def restore_animation_controls(self):
		self.animation_control_frame.run_button.configure(state ='normal')
		self.animation_control_frame.continue_button.config(state = 'normal')
		self.animation_control_frame.anim_speed_option.configure(state ='normal')
		self.cell_diagram_frame.cell_scale.configure(state = 'normal')

	#raise all tab buttons, then sink a specified button. Called whenever a tab button is clicked.
	def sink_selected_tab(self, button):
		for _ in self.tab_buttons.values():
			_.configure(relief='raised')
		self.tab_buttons[button].configure(relief='sunken')

	#Used to insure that every widget is visible after changing tabs.
	def restore_default_control_frame(self):
		for frame in self.control_frame.children.values():
			for widget in frame.children.values():
				widget.grid()
				widget.configure(state='normal')
		self.animation_control_frame.continue_button.configure(state='disabled')


	def execute_callback(self, callback_name, *args, **kwargs):
		if callback_name in self.callback_registry:
			for function in self.callback_registry[callback_name]:
				function(*args, **kwargs)
		else:
				pass

	#Stop animation, restore UI controls, clear plots. Used when changing tabs, or manually clearing plots.
	def clear_plots(self):
		self.plots_frame.clear_plots()
		self.restore_animation_controls()
		self.plots_frame.canvas.draw()

	def disable_widgets(self, frame):
		for widget in frame.children.values():
			widget.configure(state='disabled')

	def set_exercise_1(self):
		self.lattice_frame.set_lattice_inputs(10, 8, 1)
		self.particle_control_frame.set_particle_inputs(0.4, -0.1)
		self.animation_control_frame.anim_speed_option.set_speed('slow')

		self.animation_control_frame.anim_speed_option.grid_remove()
		self.animation_control_frame.continue_button.grid_remove()
		self.cell_diagram_frame.cell_diagram.grid_remove()
		self.cell_diagram_frame.cell_scale.grid_remove()

		self.lattice_frame.disable_all_widgets()

	def set_exercise_2(self):
		self.lattice_frame.set_lattice_inputs(10, 8, 12)
		self.particle_control_frame.set_particle_inputs(0.4, -0.1)
		self.animation_control_frame.anim_speed_option.set_speed('med')

		self.animation_control_frame.anim_speed_option.grid_remove()
		self.animation_control_frame.continue_button.grid_remove()
		self.cell_diagram_frame.cell_diagram.grid_remove()
		self.cell_diagram_frame.cell_scale.grid_remove()

		self.particle_control_frame.disable_all_widgets()

	def set_exercise_3(self):
		self.set_exercise_2()
		self.lattice_frame.set_lattice_inputs(10, 40, 25)
		self.particle_control_frame.set_particle_inputs(0.4, -0.1)
		self.animation_control_frame.anim_speed_option.set_speed('med')

	def set_exercise_4(self):
		self.lattice_frame.set_lattice_inputs(10, 40, 25)
		self.particle_control_frame.set_particle_inputs(0.4, -0.1)
		self.animation_control_frame.anim_speed_option.set_speed('fast')

		self.animation_control_frame.anim_speed_option.grid_remove()
		self.animation_control_frame.continue_button.grid_remove()
		self.lattice_frame.disable_all_widgets()

	def relimit_plots(self, x_max, xp_max, s_max, x_min, xp_min, s_min):
		self.plots_frame.relimit_orbit_plot(s_min, s_max, x_min, x_max)
		self.plots_frame.relimit_phase_space_plot(x_min, x_max, xp_min, xp_max) 

if __name__ == '__main__':
	view = View()
	view.main()