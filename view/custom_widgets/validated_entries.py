import tkinter as tk
import re

class ValidatedEntry(tk.Entry):
	def __init__(self, parent, validation_pattern, **kwargs):
		super().__init__(parent, **kwargs)
		self.validation_pattern = validation_pattern
		validation_function = self.register(self._validate_pattern)
		self.configure(validate='all', validatecommand = (validation_function, '%P'))

		self.valid_color = 'black'
		self.invalid_color = 'red'

		if 'fg' in kwargs or 'foreground' in kwargs:
			self.valid_color = kwargs.get('fg', kwargs.get('foreground'))

	def _validate_pattern(self, value):
		if re.fullmatch(self.validation_pattern, value) is None: #if no match
			super().configure(foreground = self.invalid_color)
			return True
		else:
			super().configure(foreground = self.valid_color)
			return True

	def configure(self, **kwargs):
		super().configure(**kwargs)
		if 'fg' in kwargs or 'foreground' in kwargs:
			self.valid_color = kwargs.get('fg', kwargs.get('foreground'))
			super().configure(fg=self.valid_color)


#DigitEntry turns text red on focus-out if the text contains anything other positive whole numbers
class DigitEntry(ValidatedEntry):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, validation_pattern=r'^[1-9]\d*$', width=12, **kwargs)

	def get(self):
		return int(super().get())

#FloatEntry turns text red on focus-out if the text contains anything other than a float
class FloatEntry(ValidatedEntry):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, validation_pattern=r'^-?\d+(\.\d+)?$', width=12, **kwargs)

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