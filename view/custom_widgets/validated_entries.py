import tkinter as tk
from tkinter import ttk
import re

#DigitEntry turns text red on focus-out if the text contains anything other positive whole numbers
class DigitEntry(tk.Entry):
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
class FloatEntry(tk.Entry):
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

if __name__ == '__main__':
	window = tk.Tk()
	digit_label = tk.Label(text='digit entry')
	digit_entry = DigitEntry(window)
	float_entry = FloatEntry(window)
	float_label = tk.Label(text='float entry')
	digit_label.pack()
	digit_entry.pack()
	float_label.pack()
	float_entry.pack()
	window.mainloop()