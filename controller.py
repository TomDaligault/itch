import tkinter as tk

from presenter.presenter import Presenter
from view.single_particle_view import SingleParticleView
from model.model import Model
from view.theme_applier import RecursiveKeyWordSetter

def apply_theme(widget, bg_color='#333333', fg_color='#526D82'):
	# Try to configure background and foreground if supported
	try:
		widget.configure(bg=bg_color)
	except tk.TclError:
		pass  # Some widgets (like ttk) won't accept bg directly

	try:
		widget.configure(fg=fg_color)
	except tk.TclError:
		pass  # Not all widgets support fg (e.g., frames)

	# Recursively apply to children
	for child in widget.winfo_children():
		apply_theme(child, bg_color=bg_color, fg_color=fg_color)

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Single Particle Dynamics')
	view = SingleParticleView(root)
	model = Model()
	presenter = Presenter(view, model)

	dark = '#282828'
	mid = '#303030'
	text = '#5f8cad' #66AD5F
	highlight = '#06FF00'
	theme_setter = RecursiveKeyWordSetter()
	theme_setter.set_widget_config(tk.Frame, bg=mid)
	theme_setter.set_widget_config(tk.Button, bg=mid, fg=text)
	theme_setter.set_widget_config(tk.Entry, bg=mid, fg=text, disabledbackground=dark)
	theme_setter.set_widget_config(tk.Label, bg=mid, fg=text)
	theme_setter.set_widget_config(tk.OptionMenu, bg=mid, fg=text)
	theme_setter.set_widget_config(tk.Menu, bg=mid, fg=text, activeforeground=text, activebackground='#484848')
	theme_setter.set_widget_config(tk.Canvas, bg=mid)
	theme_setter.set_widget_config(tk.Scale, bg=highlight, troughcolor=mid, highlightthickness=1, highlightbackground='#526D82')
	theme_setter.apply_configs(root)

	root.mainloop()