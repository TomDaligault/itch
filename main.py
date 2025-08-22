import tkinter as tk

from presenter.presenter import Presenter
from view.single_particle_view import SingleParticleView
from model.model import Model
from view.compound_widgets.transverse_plots_widget import TransversePlotsWidget
from view.theme_applier import RecursiveKeyWordSetter, RecursiveBindSetter

if __name__ == '__main__':	
	root = tk.Tk()
	root.title('Single Particle Dynamics')
	view = SingleParticleView(root)
	model = Model()
	presenter = Presenter(view, model)

	dark = '#282828'
	mid = '#303030'
	text_dark = '#5f8cad'
	text_light = '#526D82'
	highlight = '#0FF600'
	hover = '#404040'

	theme_setter = RecursiveKeyWordSetter()
	theme_setter.set_config(tk.Scale, bg=highlight, troughcolor=mid, activebackground=highlight, highlightbackground=text_light, highlightthickness=1)
	theme_setter.set_config(tk.OptionMenu, bg=mid, fg=text_dark, activeforeground=text_dark, activebackground=hover)
	theme_setter.set_config(tk.Button, bg=mid, fg=text_dark, activeforeground=text_dark, activebackground=hover)
	theme_setter.set_config(tk.Menu, bg=mid, fg=text_dark, activeforeground=text_dark, activebackground=hover)
	theme_setter.set_config(tk.Entry, bg=mid, fg=text_dark, disabledbackground=dark)
	theme_setter.set_config(tk.Label, bg=mid, fg=text_dark)
	theme_setter.set_config(tk.Canvas, bg=mid)
	theme_setter.set_config(tk.Frame, bg=mid)
	theme_setter.set_config(TransversePlotsWidget, bg=dark, fg=text_light, marker_color=highlight)
	theme_setter.apply_configs(root)

	bind_setter = RecursiveBindSetter()
	bind_setter.set_bind(tk.Button, '<Enter>', lambda event: event.widget.configure(bg=hover))
	bind_setter.set_bind(tk.Entry, '<Enter>', lambda event: event.widget.configure(bg=hover))
	bind_setter.set_bind(tk.Button, '<Leave>', lambda event: event.widget.configure(bg=mid))
	bind_setter.set_bind(tk.Entry, '<Leave>', lambda event: event.widget.configure(bg=mid))
	bind_setter.apply_binds(root)
	root.mainloop()