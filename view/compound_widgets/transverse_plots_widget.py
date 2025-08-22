import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TransversePlotsWidget(tk.Frame):

	line_kwargs = {'linewidth': 0.5}

	scatter_kwargs = {'color':'None', 's': 50}
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

		self.orbit_line, = self.orbit_plot.plot([],[], marker='o', animated = True, **self.line_kwargs)
		self.orbit_scatter = self.orbit_plot.scatter([],[], animated = True, **self.scatter_kwargs)

		self.phase_space_plot.set_title('phase space plot')
		self.phase_space_plot.set_xlabel('x')
		self.phase_space_plot.set_ylabel('x\'', rotation = 0)

		self.phase_space_line, = self.phase_space_plot.plot([],[], marker='o', animated = True,**self.line_kwargs)
		self.phase_space_scatter = self.phase_space_plot.scatter([],[], animated = True, **self.scatter_kwargs)

		self._set_default_plot_limits()

		self.figure.tight_layout(pad=1.6)

	def configure(self, **kwargs):
		if 'bg' in kwargs or 'background' in kwargs:
			bg_color = kwargs.pop('bg', kwargs.pop('background', None))
			self.figure.set_facecolor(bg_color)
			for plot in self.figure.get_axes():
				plot.set_facecolor(bg_color)

		if 'fg' in kwargs or 'foreground' in kwargs:
			fg_color = kwargs.pop('fg', kwargs.pop('foreground', None))
			self.orbit_scatter.set_edgecolors(fg_color)
			self.phase_space_scatter.set_edgecolors(fg_color)
			self.orbit_line.set_color(fg_color)
			self.phase_space_line.set_color(fg_color)
			self.line_kwargs['color'] = fg_color
			for plot in self.figure.get_axes():
				plot.title.set_color(fg_color)
				plot.xaxis.label.set_color(fg_color)
				plot.yaxis.label.set_color(fg_color)
				plot.tick_params(colors=fg_color)

				for spine in plot.spines.values():
					spine.set_color(fg_color)

		if 'marker_color' in kwargs:
			marker_color = kwargs.pop('marker_color', None)
			self.line_kwargs['markerfacecolor'] = marker_color
			self.line_kwargs['markeredgecolor'] = marker_color
			self.orbit_line.set_markerfacecolor(marker_color)
			self.orbit_line.set_markeredgecolor(marker_color)
			self.phase_space_line.set_markerfacecolor(marker_color)
			self.phase_space_line.set_markeredgecolor(marker_color)

		super().configure(**kwargs)


	def relimit_orbit_plot(self, smin, smax, xmin, xmax):
		current_smin, current_smax, current_xmin, current_xmax = self.orbit_plot.axis()

		#check if data will exceed current plot limits, adjust plot limits if necessary
		if current_smin > smin:
			self.orbit_plot.set_xlim(xmin = smin)

		if current_smax < smax:
			self.orbit_plot.set_xlim(xmax = smax)

		if current_xmin > xmin:
			self.orbit_plot.set_ylim(ymin = xmin*1.1)

		if current_xmax < xmax:
			self.orbit_plot.set_ylim(ymax = xmax*1.1)

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
		if not(len(x_data) == len(xp_data) == len(s_data)):
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
		self.canvas.draw()
		self._reset_animated_lines()

	def _reset_animated_lines(self):
		self.orbit_line.set_data([],[])
		self.phase_space_line.set_data([],[])

	def clone_line(self, line):
		return Line2D(line.get_xdata(), line.get_ydata(), animated=False, marker=line.get_marker(), markevery=line.get_markevery(), **self.line_kwargs)

	def pause_animation(self):
		try:
			self.animation.pause()
		except AttributeError:
			pass

	def clear_plots(self):
		#pause animation and clear current data
		self.pause_animation() #clearing while the animation is still running would cause errors 
		self._reset_animated_lines()
		#matplotlib scatters cannot easily have their data set to none, so I just move them out of bounds
		self.orbit_scatter.set_offsets([-1,-1])
		self.phase_space_scatter.set_offsets([-1,-1])

		#remove stored lines
		for line in self.previous_lines:
				line.remove()

		#clear history
		self.previous_lines = []

		self._set_default_plot_limits()
		self.canvas.draw()

	def _set_default_plot_limits(self):
		self.orbit_plot.set(xlim=(-0.1, 0.1), ylim=(-0.1, 0.1))
		self.phase_space_plot.set(xlim=(-0.1, 0.1), ylim=(-0.1, 0.1))

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
