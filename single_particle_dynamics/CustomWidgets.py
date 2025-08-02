import tkinter as tk
from tkinter import ttk
import re

import matplotlib.pyplot 

#DigitEntry turns text red on focus-out if the text contains anything other positive whole numbers
class DigitEntry(ttk.Entry):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, width=12, **kwargs)
		validation_function = self.register(self._validate_digit)
		self.configure(validate='focusout', validatecommand = (validation_function, '%P'))

	def _validate_digit(self, value):
		pattern = r'^[1-9]\d*$'
		if re.fullmatch(pattern, value) is None: #if no match
			self.configure(foreground ='red')
			return False
		else:
			self.configure(foreground ='black')
			return True

	def get(self):
		return int(super().get())

#FloatEntry turns text red on focus-out if the text contains anything other than a float
class FloatEntry(ttk.Entry):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, width=12, **kwargs)
		validation_function = self.register(self._validate_float)
		self.configure(validate='focusout', validatecommand = (validation_function, '%P'))

	def _validate_float(self, value):
		pattern = r'^-?\d+(\.\d+)?$'
		if re.fullmatch(pattern, value) is None: #if no match
			self.configure(foreground ='red')
			return False
		else:
			self.configure(foreground ='black')
			return True

	def get(self):
		return float(super().get())

#CellDiagram is a canvas object using rectangles and ovals to make a rough FODO cell diagram
class CellDiagram(tk.Canvas):
	def __init__(self, parent, width=200, height=100, **kwargs):
		super().__init__(parent, width=width, height=height, **kwargs)

		# Store the dimensions and radius
		x_offset = width/6
		y_offset = height/20
		#draw the focusing quad
		self.create_oval(2 +width/20, 2, width/4 + 2 - width/20, height+1, fill='#b5eef7', width=0)
		self.create_rectangle(2, 2, width/4 + 2, height+1)

		#draw the defocusing quad
		self.create_rectangle(2 + width/2, 2, 3*width/4, height+4, fill='#b5eef7', width=0)
		self.create_oval(2 + width/2 - x_offset, -y_offset/2, 3*width/4 - x_offset, height + y_offset/2 + 3, fill='#F0F0F0', width=0)
		self.create_oval(2 + width/2 + x_offset, -y_offset/2, 3*width/4 + x_offset, height + y_offset/2 + 3, fill='#F0F0F0', width=0)
		self.create_rectangle(2 + width/2, 2, 3*width/4 + 2, height+1)

#A pre-configured tkinter scale. Changes color if disabled.
class CellScale(tk.Scale):
	def __init__(self, parent, color='#d9544f', **kwargs):
		super().__init__(parent, **kwargs)
		self.color = color
		state = kwargs.get('state', 'normal')
		self.configure(length=200, width=8, bd=0, resolution=1, state=state,
								   showvalue = False, orient = 'horizontal', bg=self.color, troughcolor = '#e6e6e6',
								   sliderlength=5)

	def configure(self, **kwargs):
		if 'state' in kwargs:
			state = kwargs['state']
			if state == 'disabled':
				super().configure(bg = '#F0F0F0')
			else:
				super().configure(bg = self.color)
		super().configure(**kwargs)

class PlaySpeedOptionMenu(tk.OptionMenu):
	anim_speeds = {'fast': 0, 'med': 6, 'slow': 30}

	def __init__(self, master, **kwargs):
		self.speed_var = tk.StringVar(value='fast')
		super().__init__(master, self.speed_var, *self.anim_speeds.keys(), **kwargs)

	def set_speed(self, speed):
		if speed in self.anim_speeds:
			self.speed_var.set(speed)
	
	def get_speed(self):
		return self.anim_speeds.get(self.speed_var.get(), 0)
