import tkinter as tk
from .base_frame import BaseFrame
from view.custom_widgets import StateAwareScale

#CellElementSelector contains a tkinter canvas with a crude FODO cell diagram and an overlaid StateAwareScale
#On change, the scale will execute any functions associated with 'on_cell_scale_change' in the callback_registry, if provided
class CellElementSelector(BaseFrame):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		self.cell_diagram = CellDiagram(self)
		#By default, tkinter scales pass their current value as an argument to their command.
		#Rather than deal with the built in, this lambda function throws away the argument.
		#Callback functions should call scale.get() if they need the current value.
		self.cell_scale = StateAwareScale(self, command=lambda _: self._execute_callback('on_cell_scale_change'))

		self.cell_diagram.grid(row = 0, column = 0)
		self.cell_scale.grid(row = 0, column = 0)

	def get_scale_value(self):
		return int(self.cell_scale.get())

	def set_scale_value(self, value):
		return self.cell_scale.set(value)

	def set_scale_length(self, scale_length):
		self.cell_scale.configure(to=scale_length)

	def set_colors(self, background, enabled, disabled, trough, quads):
		self.cell_scale.set_colors(enabled, disabled, trough)
		self.cell_scale.configure(bg=enabled)
		self.cell_diagram.set_colors(quads, background)


#CellDiagram is a canvas object using rectangles and ovals to make a rough FODO cell diagram
class CellDiagram(tk.Canvas):
	def __init__(self, parent, width=200, height=100, **kwargs):
		super().__init__(parent, highlightthickness=0, width=width, height=height, **kwargs)

		# Store the dimensions and radius
		x_offset = width/6
		y_offset = height/20
		#draw the focusing quad
		self.f_quad = self.create_oval(2 +width/20, 4, width/4 + 2 - width/20, height-2, fill='#526D82', width=0)
		self.create_rectangle(2, 2, width/4 + 2, height-1, outline='#050505')

		#draw the defocusing quad
		self.d_quad = self.create_rectangle(2 + width/2, 4, 3*width/4, height-2, fill='#526D82', width=0)
		self.bg1 = self.create_oval(2 + width/2 - x_offset, -y_offset/2, 3*width/4 - x_offset+1, height + y_offset/2 + 2, fill='#303030', width=0)
		self.bg2 = self.create_oval(2 + width/2 + x_offset, -y_offset/2, 3*width/4 + x_offset+1, height + y_offset/2 + 2, fill='#303030', width=0)
		self.create_rectangle(2 + width/2, 2, 3*width/4 + 2, height-1, outline='#050505')

	def set_colors(self, quads, background):
		self.configure(bg=background)
		self.itemconfigure(self.f_quad, fill=quads)
		self.itemconfigure(self.d_quad, fill=quads)

		self.itemconfigure(self.bg1, fill=background)
		self.itemconfigure(self.bg2, fill=background)