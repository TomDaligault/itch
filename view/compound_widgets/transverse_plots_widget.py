import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..custom_widgets.base_frame import BaseFrame

class TransversePlotsWidget(BaseFrame):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		#custom keyword support
		self._configure_registry = {
			"marker_color": self.set_marker_color,
			"background": self.set_background_color,
			"foreground": self.set_foreground_color,
			"bg": self.set_background_color,
			"fg": self.set_foreground_color,
			}

		self.register_callback_name('on_animation_complete')

		self.line_kwargs = {'linewidth': 0.5, 'marker':'o', 'markeredgecolor': 'None', 'markevery': 20}
		self.scatter_kwargs = {'color':'None', 's': 50}
		self.animation_interval = 0 #units are milliseconds per frame

		self.figure = Figure(figsize=(8.4, 4))
		self.orbit_plot = self.figure.add_subplot(1, 2, 1)
		self.phase_space_plot = self.figure.add_subplot(1, 2, 2)

		self.canvas = FigureCanvasTkAgg(self.figure, master=self)
		self.canvas_widget = self.canvas.get_tk_widget()
		self.canvas_widget.pack(fill='both', expand=True)

		self.orbit_plot.set_title('orbit plot')
		self.orbit_plot.set_xlabel('s')
		self.orbit_plot.set_ylabel('x', rotation = 0)

		self.phase_space_plot.set_title('phase space plot')
		self.phase_space_plot.set_xlabel('x')
		self.phase_space_plot.set_ylabel('x\'', rotation = 0)

		self._set_default_plot_limits()
		self.figure.tight_layout(pad=1.6)

	def set_background_color(self, color):
		self.figure.set_facecolor(color)
		for plot in self.figure.get_axes():
			plot.set_facecolor(color)

	def set_foreground_color(self, color):
		self.line_kwargs['color'] = color
		self.scatter_kwargs['edgecolors'] = color

		for plot in self.figure.get_axes():
			plot.title.set_color(color)
			plot.xaxis.label.set_color(color)
			plot.yaxis.label.set_color(color)
			plot.tick_params(colors=color)

			#handles bounding boxes of the plots
			for spine in plot.spines.values():
				spine.set_color(color)

	def set_marker_color(self, color):
		self.line_kwargs['markerfacecolor'] = color

	def set_marker_spacing(self, spacing):
		self.line_kwargs['markevery'] = spacing

	def set_marker_visibility(self, is_visible):
		if is_visible:
			self.line_kwargs['marker'] = 'o'
		else:	
			self.line_kwargs['marker'] = 'None'

	def set_markers(self, marker_start):
		for line in self.orbit_plot.get_lines():
			line.set_markevery((marker_start, self.line_kwargs['markevery']))

		for line in self.phase_space_plot.get_lines():
			line.set_markevery((marker_start, self.line_kwargs['markevery']))

		self.canvas.draw()

	def set_animation_interval(self, interval):
		self.animation_interval = interval

	def plot_data(self, x_data, xp_data, s_data):
		self.orbit_plot.plot(s_data, x_data, **self.line_kwargs)
		self.phase_space_plot.plot(x_data, xp_data, **self.line_kwargs)
		self.canvas.draw()

	def animate_data(self, x_data, xp_data, s_data):
		#check data lengths
		if not(len(x_data) == len(xp_data) == len(s_data)):
			raise ValueError("All data must have the same length")

		#initialize artists for animation
		orbit_line, = self.orbit_plot.plot([],[], animated = True, **self.line_kwargs)
		phase_space_line, = self.phase_space_plot.plot([],[], animated = True,**self.line_kwargs)
		orbit_scatter = self.orbit_plot.scatter([],[], animated = True, **self.scatter_kwargs)
		phase_space_scatter = self.phase_space_plot.scatter([],[], animated = True, **self.scatter_kwargs)

		#define the animation function
		#Called for each frame of FuncAnimation. Must return an iterable of artists for blitting
		def update(frame):
			orbit_line.set_data(s_data[:frame+1], x_data[:frame+1])
			phase_space_line.set_data(x_data[:frame+1], xp_data[:frame+1])
			orbit_scatter.set_offsets([s_data[frame], x_data[frame]])
			phase_space_scatter.set_offsets([x_data[frame], xp_data[frame]])

			if frame == len(x_data) - 1:
				self._execute_callback('on_animation_complete')

			return orbit_line, phase_space_line, orbit_scatter, phase_space_scatter

		self.animation = animation.FuncAnimation(fig = self.figure,
									  func = update,
									  frames = len(x_data),
									  interval = self.animation_interval,
									  repeat = False,
									  blit = True)

		# return orbit_line, phase_space_line, orbit_scatter, phase_space_scatter

	def pause_animation(self):
		try:
			self.animation.pause()
		except AttributeError:
			pass

	def clear_plots(self):
		#pause animation to avoid throwing errors
		self.pause_animation() 

		for ax in (self.orbit_plot, self.phase_space_plot):
			for line in list(ax.get_lines()):
				line.remove()
			for coll in list(ax.collections):
				coll.remove()

		self._set_default_plot_limits()
		self.canvas.draw()

	def _set_default_plot_limits(self):
		self.orbit_plot.set(xlim=(-0.1, 0.1), ylim=(-0.1, 0.1))
		self.phase_space_plot.set(xlim=(-0.1, 0.1), ylim=(-0.1, 0.1))

	#check if data will exceed current plot limits, adjust plot limits if necessary
	def relimit_orbit_plot(self, smin, smax, xmin, xmax):
		current_smin, current_smax, current_xmin, current_xmax = self.orbit_plot.axis()
		if current_smin > smin:
			self.orbit_plot.set_xlim(xmin = smin)
		if current_smax < smax:
			self.orbit_plot.set_xlim(xmax = smax)
		if current_xmin > xmin:
			self.orbit_plot.set_ylim(ymin = xmin*1.1)
		if current_xmax < xmax:
			self.orbit_plot.set_ylim(ymax = xmax*1.1)

	#check if data will exceed current plot limits, adjust plot limits if necessary
	def relimit_phase_space_plot(self, xmin, xmax, xpmin, xpmax):
		current_xmin, current_xmax, current_xpmin, current_xpmax = self.phase_space_plot.axis()
		if current_xmin > xmin:
			self.phase_space_plot.set_xlim(xmin = xmin*1.2)
		if current_xmax < xmax:
			self.phase_space_plot.set_xlim(xmax = xmax*1.2)
		if current_xpmin > xpmin:
			self.phase_space_plot.set_ylim(ymin = xpmin*1.2)
		if current_xpmax < xpmax:
			self.phase_space_plot.set_ylim(ymax = xpmax*1.2)