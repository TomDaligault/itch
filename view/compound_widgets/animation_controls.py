import tkinter as tk
from .base_frame import BaseFrame
from view.custom_widgets.speed_menu import SpeedMenu

class AnimationControls(BaseFrame):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		self.run_button = tk.Button(self, text="run", command=lambda: self._execute_callback('run_animation'))
		self.continue_button = tk.Button(self, text="continue", state='disabled', command=lambda: self._execute_callback('continue_animation'))
		self.clear_button = tk.Button(self, text="clear", command=lambda: self._execute_callback('clear'))
		self.speed_menu = SpeedMenu(self)
		self.speed_menu.configure(highlightthickness=0)

		self.speed_menu.grid(row = 0, column = 0)
		self.run_button.grid(row = 0, column = 1)
		self.continue_button.grid(row = 0, column = 2)
		self.clear_button.grid(row = 0, column = 3)

	def get_speed(self):
		return self.speed_menu.get_speed()

	def set_speed(self, speed):
		self.speed_menu.set_speed(speed)