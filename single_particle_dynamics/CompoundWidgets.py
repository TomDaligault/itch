import tkinter as tk
import CustomWidgets
from typing import Callable

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


'''CompoundWidgets are extensions of tkinter Frame that come pre-loaded with tkinter widgets.'''
'''All custom frames inherit from a base class with methods for toggling widget state and visibility.'''
'''All widgets placed inside of any CompoundWidget must be placed using .grid(**kwargs).'''
'''Commands are supported via optionally providing a callback registry.'''
'''Widgets in frames will check the registry for their assigned callback_name and execute all associated functions'''
'''I am told that this registry acts like an event bus. Will consider seperating developing a seperate module for this.'''

#Considering changing callback_names formatting to match tkinter events.
#Should add a list of expected callback_names somewhere
class BaseFrame(tk.Frame):
	def __init__(self, parent: tk.Frame, callback_registry: dict[str, list[Callable]] = None, **kwargs):
		super().__init__(parent, **kwargs)
		self.callback_registry = callback_registry or {}

	def _execute_callback(self, callback_name, *args, **kwargs):
		if not self.callback_registry: #Check that the registry is not empty
			raise ValueError(f"Callback registry is empty, please provide a callback registry.")

		if callback_name not in self.callback_registry: #Check that the callback is registered
			raise KeyError(f"Callback name '{callback_name}' not found in registry.")

		callback_functions = self.callback_registry[callback_name]

		if not callback_functions: #Check that the callback has associated functions
			raise ValueError(f"Callback name '{callback_name}' has no associated functions")

		for function in callback_functions: #execute all associated functions 
			function(*args, **kwargs)

	def show_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.grid()
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def hide_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.grid_remove()
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def enable_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.configure(state='normal')
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def disable_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.configure(state='disabled')
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def enable_all_widgets(self):
		for widget in self.winfo_children():
			try: 
				widget.configure(state='normal')
			except (tk.TclError, TypeError):
				pass # Widget may not support 'state'; skip it

	def disable_all_widgets(self):
		for widget in self.winfo_children():
			try: 
				widget.configure(state='disabled')
			except (tk.TclError, TypeError):
				pass # Widget may not support 'state'; skip it

class TabsFrame(BaseFrame):
	def __init__(self, parent, tab_names: list[str], **kwargs):
		super().__init__(parent, **kwargs)
		self.tab_names = tab_names
		self.tab_buttons = {}

		#Dynamically create buttons from tab_names and add them to a dictionary
		#All buttons share the same callback function. Each button passes its specific name to the callback when clicked.
		for button_name in self.tab_names:
			button = tk.Button(self, text=button_name, command=lambda n=button_name: [self.sink_selected_tab(n), self._execute_callback('on_tab_change', n)])
			self.tab_buttons[button_name] = button
			button.pack(side='left', expand=True, fill='x')

	#raise all tab buttons, then sink a specified button. Called whenever a tab button is clicked.
	def sink_selected_tab(self, button):
		for _ in self.tab_buttons.values():
			_.configure(relief='raised')
		self.tab_buttons[button].configure(relief='sunken')

class LatticeDiagramFrame(BaseFrame):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		self.cell_diagram = CustomWidgets.CellDiagram(self)
		#By default, tkinter scales pass their current value as an argument to their command.
		#Rather than deal with the built in, this lambda function throws away the argument.
		#Callback functions should call scale.get() if they need the current value.
		self.cell_scale = CustomWidgets.CellScale(self, command=lambda _: self._execute_callback('on_cell_scale_change'))

		self.cell_diagram.grid(row = 0, column = 0)
		self.cell_scale.grid(row = 0, column = 0)

class AnimationControlFrame(BaseFrame):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		self.run_button = tk.Button(self, text="run", command=lambda: self._execute_callback('run_animation'))
		self.continue_button = tk.Button(self, text="continue", state='disabled', command=lambda: self._execute_callback('continue_animation'))
		self.clear_button = tk.Button(self, text="clear", command=lambda: self._execute_callback('clear_plots'))
		self.anim_speed_option = CustomWidgets.PlaySpeedOptionMenu(self)

		self.anim_speed_option.grid(row = 0, column = 0)
		self.run_button.grid(row = 0, column = 1)
		self.continue_button.grid(row = 0, column = 2)
		self.clear_button.grid(row = 0, column = 3)

class TransversePlotsWidget(tk.Frame):
	line_kwargs = {'linewidth': 0.5, 'markerfacecolor': '#d9544f', 'markeredgecolor': '#d9544f', 'color': 'gray'}
	previous_lines = []
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.animation_interval = 0 #units of milliseconds per frame
		
		self.figure = Figure(figsize=(8.4, 4))
		self.orbit_plot = self.figure.add_subplot(1, 2, 1)
		self.phase_space_plot = self.figure.add_subplot(1, 2, 2)

		self.canvas = FigureCanvasTkAgg(self.figure, master=self)
		self.canvas_widget = self.canvas.get_tk_widget()
		self.canvas_widget.pack(fill='both', expand=True)

		self.orbit_plot.set_title('orbit plot')
		self.orbit_plot.set_xlabel('s')
		self.orbit_plot.set_ylabel('x', rotation = 0)
		self.orbit_line, = self.orbit_plot.plot([],[], marker='o', animated=True, **self.line_kwargs)
		self.orbit_scatter = self.orbit_plot.scatter([],[], color='None', edgecolors = '#d9544f', s=50, animated=True)

		self.phase_space_plot.set_title('phase space plot')
		self.phase_space_plot.set_xlabel('x')
		self.phase_space_plot.set_ylabel('x\'', rotation = 0)
		self.phase_space_line, = self.phase_space_plot.plot([],[], marker='o', animated=True, **self.line_kwargs)
		self.phase_space_scatter = self.phase_space_plot.scatter([],[], color='None', edgecolors = '#d9544f', s=50, animated=True)

		self.orbit_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))
		self.phase_space_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))

		self.figure.tight_layout(pad=1.6)
		matplotlib.pyplot.tight_layout()

	def relimit_orbit_plot(self, smin, smax, xmin, xmax):
		current_smin, current_smax, current_xmin, current_xmax = self.orbit_plot.axis()

		#check if data will exceed current plot limits, adjust plot limits if necessary
		if current_smin > smin:
			self.orbit_plot.set_xlim(xmin = smin)

		if current_smax < smax:
			self.orbit_plot.set_xlim(xmax = smax)

		if current_xmin > xmin:
			self.orbit_plot.set_ylim(ymin = xmin - 0.5)

		if current_xmax < xmax:
			self.orbit_plot.set_ylim(ymax = xmax + 0.5)

	def relimit_phase_space_plot(self, xmin, xmax, xpmin, xpmax):
		current_xmin, current_xmax, current_xpmin, current_xpmax = self.phase_space_plot.axis()

		#check if data will exceed current plot limits, adjust plot limits if necessary
		if current_xmin > xmin:
			self.phase_space_plot.set_xlim(xmin = xmin*1.2)

		if current_xmax < xmax:
			self.phase_space_plot.set_xlim(xmax = xmax*1.2)

		if current_xpmin > xpmin:
			self.phase_space_plot.set_ylim(ymin = xpmin*1.2)

		if current_xpmax < xpmax:
			self.phase_space_plot.set_ylim(ymax = xpmax*1.2)

	def set_animation_interval(self, interval):
		self.animation_interval = interval

	def animate_plots(self, x_data, xp_data, s_data, callback=None):
		if not(len(x_data) == len(x_data) == len(x_data)):
			raise ValueError("All data must have the same length")

		self.animation = animation.FuncAnimation(fig = self.figure,
									  func = self.animation_fuction,
									  fargs = (x_data, xp_data, s_data, callback),
									  frames = len(x_data),
									  interval = self.animation_interval,
									  repeat = False,
									  blit = True)

	#Called for each frame of FuncAnimation. Must return an iterable of artists for blitting
	def animation_fuction(self, frame, x_data, xp_data, s_data, callback):
		self.orbit_line.set_data(s_data[:frame+1], x_data[:frame+1])
		self.phase_space_line.set_data(x_data[:frame+1], xp_data[:frame+1])

		self.orbit_scatter.set_offsets([s_data[frame], x_data[frame]])
		self.phase_space_scatter.set_offsets([x_data[frame], xp_data[frame]])

		if frame == max(range(len(x_data))):
			#cache lines and clear current
			self.cache_lines()

			if callback:
				callback() #Execute callback if provided

		return self.orbit_line, self.phase_space_line, self.orbit_scatter, self.phase_space_scatter

	def cache_lines(self):
		#Current lines is copied and added to plots, letting matplotlib handle memory management of previous animation results.
		line = self.clone_line(self.orbit_line)
		self.orbit_plot.add_line(line)
		self.previous_lines.append(line)

		line = self.clone_line(self.phase_space_line)
		self.phase_space_plot.add_line(line)
		self.previous_lines.append(line)

	def clone_line(self, line):
		return Line2D(line.get_xdata(), line.get_ydata(), marker=line.get_marker(), markevery=line.get_markevery(), **self.line_kwargs)

	def pause_animation(self):
		try:
			self.animation.pause()
		except AttributeError:
			pass

	def clear_plots(self):
		#pause animation and clear current data
		self.pause_animation() #clearing while the animation is still running would cause errors 
		self.orbit_line.set_data([],[])
		self.phase_space_line.set_data([],[])
		self.orbit_scatter.set_offsets([0,0])
		self.phase_space_scatter.set_offsets([0,0])

		#remove stored lines
		for line in self.previous_lines:
				line.remove()

		#clear history
		self.previous_lines = []

		#set default plot boundaries
		self.orbit_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))
		self.phase_space_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))

	def set_markers(self, marker_start, marker_spacing):
		for line in self.orbit_plot.get_lines():
			line.set_markevery((marker_start, marker_spacing))

		for line in self.phase_space_plot.get_lines():
			line.set_markevery((marker_start, marker_spacing))

		self.canvas.draw()

	def hide_markers(self):
		self.orbit_line.set_marker('None')
		self.phase_space_line.set_marker('None')

	def show_markers(self):
		self.orbit_line.set_marker('o')
		self.phase_space_line.set_marker('o')

class ParticleControlFrame(BaseFrame):
	default_particle_parameters = {'x': 0.4, 'xp': -0.1}

	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		self.x_entry = CustomWidgets.FloatEntry(self)
		self.xp_entry = CustomWidgets.FloatEntry(self)
		self.randomize_button = tk.Button(self, text='randomize', command=lambda: self._execute_callback('randomize_particle'))

		tk.Label(self, text='Initial x').grid(row=0, column=0)
		tk.Label(self, text='Initial x\'').grid(row=1, column=0)
		self.x_entry.grid(row=0, column=1)
		self.xp_entry.grid(row=1, column=1)
		self.randomize_button.grid(row=2, column=0, columnspan=2, sticky='WE')

		#set default values
		self.set_particle_inputs(*list(self.default_particle_parameters.values()))

	def set_particle_inputs(self, x, xp):
		self.x_entry.delete(0, tk.END)
		self.xp_entry.delete(0, tk.END)
		self.x_entry.insert(0, x)
		self.xp_entry.insert(0, xp)

	def get_particle_inputs(self):
		return self.x_entry.get(), self.xp_entry.get()

class LatticeControlFrame(BaseFrame):
	default_lattice_parameters = {'drift_length': 10, 'focal_length': 8, 'num_cells': 12}

	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		self.drift_entry = CustomWidgets.FloatEntry(self)
		self.focus_entry = CustomWidgets.FloatEntry(self)
		self.cell_entry = CustomWidgets.DigitEntry(self)

		tk.Label(self, text='drift length').grid(row = 0, column = 0)
		tk.Label(self, text='focal length').grid(row = 0, column = 1)
		tk.Label(self, text='num cells').grid(row = 0, column = 2)
		self.drift_entry.grid(row = 1, column = 0)
		self.focus_entry.grid(row = 1, column = 1)
		self.cell_entry.grid(row = 1, column = 2)

		#set default values
		self.set_lattice_inputs(*list(self.default_lattice_parameters.values()))

	def set_lattice_inputs(self, drift_length, focal_length, num_cells):		
		self.drift_entry.delete(0, tk.END)
		self.focus_entry.delete(0, tk.END)
		self.cell_entry.delete(0, tk.END)
		self.drift_entry.insert(0, drift_length)
		self.focus_entry.insert(0, focal_length)
		self.cell_entry.insert(0, num_cells)

	def get_lattice_inputs(self):
		return self.drift_entry.get(), self.focus_entry.get(), self.cell_entry.get()

if __name__ == '__main__':
	window = tk.Tk()
	frame = LatticeControlFrame(window)
	plots = TransversePlotsWidget(window)
	frame.pack()
	plots.pack()
	window.mainloop()