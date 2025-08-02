import tkinter as tk
'''
RecursiveKeyWordSetter is used to recursively configure keywords for all children and sub-children of some tkinter widget.
Also supports calling arb
'''
class RecursiveKeyWordSetter:
	def __init__(self):
		self.class_config_map = {}

	def set_widget_config(self, widget_class, **kwargs):
		self.class_config_map[widget_class] = kwargs


	def apply_configs(self, widget):
		for widget_class, kwargs_dict in self.class_config_map.items():
			if isinstance(widget, widget_class):
				try:
					widget.configure(**kwargs_dict)
				except tk.TclError as e:
				    print(f"Skipping widget {widget} due to invalid config: {e}")

		child_widgets = widget.winfo_children()
		for child in child_widgets:
			self.apply_configs(child)


if __name__ == '__main__':
	root = tk.Tk()

	frame = tk.Frame(root)
	frame2 = tk.Frame(root)
	button = tk.Button(frame, text='button')
	entry = tk.Entry(frame2)

	frame.pack(expand=True, fill='both')
	frame2.pack(expand=True, fill='both')
	button.pack()
	entry.pack(padx=20, pady=20)

	setter = RecursiveKeyWordSetter()
	setter.set_widget_config(tk.Frame, bg='black')
	setter.set_widget_config(tk.Button, bg='lightblue')
	setter.apply_configs(root)
	setter.set_widget_config(tk.Frame, bg='gray')
	setter.apply_configs(frame)
	color = root.winfo_rgb('SystemDisabledText')

	# Convert 16-bit per channel RGB to 8-bit hex
	hex_color = '#%02x%02x%02x' % tuple(c // 256 for c in color)

	print("Resolved color:", hex_color)
	root.mainloop()