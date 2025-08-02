import tkinter as tk

class StateAwareScale(tk.Scale):
	def __init__(self, parent, enabled_color='#d9544f', **kwargs):
		super().__init__(parent, **kwargs)
		self.enabled_color = enabled_color

		state = kwargs.get('state', 'normal')

		self.configure(length=200, width=8, bd=0, state=state,
								   showvalue=False, orient='horizontal', bg=self.enabled_color,
								   sliderlength=5)

	def configure(self, **kwargs):
		if 'bg' in kwargs or 'background' in kwargs:
		    self.enabled_color = kwargs.get('bg', kwargs.get('background'))
		if 'state' in kwargs:
			state = kwargs['state']
			if state == 'disabled':
				super().configure(bg='SystemDisabledText')
			else:
				super().configure(bg=self.enabled_color)

		super().configure(**kwargs)