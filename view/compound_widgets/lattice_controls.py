import tkinter as tk
from .base_frame import BaseFrame
from view.custom_widgets import DigitEntry, FloatEntry

class LatticeControls(BaseFrame):

	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		default_lattice_parameters = {'drift_length': 10, 'focal_length': 8, 'num_cells': 12}

		self.drift_entry = FloatEntry(self)
		self.focus_entry = FloatEntry(self)
		self.cell_entry = DigitEntry(self)

		tk.Label(self, text='drift length').grid(row = 0, column = 0)
		tk.Label(self, text='focal length').grid(row = 0, column = 1)
		tk.Label(self, text='num cells').grid(row = 0, column = 2)
		self.drift_entry.grid(row = 1, column = 0)
		self.focus_entry.grid(row = 1, column = 1)
		self.cell_entry.grid(row = 1, column = 2)

		#set default values
		self.set_lattice_inputs(*list(default_lattice_parameters.values()))

	def set_lattice_inputs(self, drift_length, focal_length, num_cells):		
		self.drift_entry.delete(0, tk.END)
		self.focus_entry.delete(0, tk.END)
		self.cell_entry.delete(0, tk.END)
		self.drift_entry.insert(0, drift_length)
		self.focus_entry.insert(0, focal_length)
		self.cell_entry.insert(0, num_cells)

	def get_lattice_inputs(self):
		return self.drift_entry.get(), self.focus_entry.get(), self.cell_entry.get()
