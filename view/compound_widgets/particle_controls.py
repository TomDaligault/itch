import tkinter as tk
from .base_frame import BaseFrame
from view.custom_widgets import DigitEntry, FloatEntry

class ParticleControls(BaseFrame):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		default_particle_parameters = {'x': 0.4, 'xp': -0.1}

		self.x_entry = FloatEntry(self)
		self.xp_entry = FloatEntry(self)
		self.randomize_button = tk.Button(self, text='randomize', command=lambda: self._execute_callback('randomize_particle'))

		tk.Label(self, text='Initial x').grid(row=0, column=0)
		tk.Label(self, text='Initial x\'').grid(row=1, column=0)
		self.x_entry.grid(row=0, column=1)
		self.xp_entry.grid(row=1, column=1)
		self.randomize_button.grid(row=2, column=0, columnspan=2, sticky='WE')

		#set default values
		self.set_particle_inputs(*list(default_particle_parameters.values()))

	def set_particle_inputs(self, x, xp):
		self.x_entry.delete(0, tk.END)
		self.xp_entry.delete(0, tk.END)
		self.x_entry.insert(0, x)
		self.xp_entry.insert(0, xp)

	def get_particle_inputs(self):
		return self.x_entry.get(), self.xp_entry.get()