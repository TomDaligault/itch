import tkinter as tk

'''SpeedMenu extends tkinter OptionMenu, intended to give user-control over the FuncAnimation interval argument'''
'''Comes with a built in dictionary mapping strings to time intervals in milliseconds'''
class SpeedMenu(tk.OptionMenu):
	def __init__(self, master, **kwargs):
		self.speed_map = {'fast': 0, 'med': 6, 'slow': 30} #Consider decoupling logic out of the widget
		self.speed_var = tk.StringVar(value='fast')
		super().__init__(master, self.speed_var, *self.speed_map.keys(), **kwargs)
		
	def set_speed(self, speed):
		if speed in self.speed_map:
			self.speed_var.set(speed)
		else:
			raise ValueError(f'{speed} not defined in map')
	
	def get_speed(self):
		try:
			return self.speed_map[self.speed_var.get()]
		except KeyError:
			raise ValueError(f"Speed option not defined")

if __name__ == '__main__':
	window = tk.Tk()
	menu = SpeedMenu(window)
	label = tk.Label(text=f'{menu.speed_var.get()}: {menu.get_speed()}ms per frame')
	menu.speed_var.trace_add("write", lambda *args: label.configure(text=f'{menu.speed_var.get()}: {menu.get_speed()}ms per frame'))

	menu.pack()
	label.pack()
	window.mainloop()