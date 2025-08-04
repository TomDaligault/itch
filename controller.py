import tkinter as tk

from presenter.presenter import Presenter
from view.single_particle_view import SingleParticleView
from model.model import Model
from view.compound_widgets.transverse_plots_widget import TransversePlotsWidget
from view.theme_applier import RecursiveKeyWordSetter, RecursiveBindSetter

if __name__ == '__main__':	
	root = tk.Tk()
	# root.overrideredirect(True)
	# title_bar = tk.Frame(root, bg="darkblue", relief="raised", bd=0)
	# title_bar.pack(side='top', expand=1, fill="x")
	# button = tk.Button(title_bar, text='button')
	# button.pack()
	# drag_offset = {'x': 0, 'y': 0}
	# title_bar.bind("<Button-1>", lambda e: (drag_offset.update({'x': e.x_root - root.winfo_x(),'y': e.y_root - root.winfo_y()})))
	# title_bar.bind("<B1-Motion>", lambda e: root.geometry(f"+{e.x_root - drag_offset['x']}+{e.y_root - drag_offset['y']}"))


	root.title('Single Particle Dynamics')
	view = SingleParticleView(root)
	model = Model()
	presenter = Presenter(view, model)

	dark = '#282828'
	mid = '#303030'
	text = '#5f8cad' #66AD5F

	highlight = '#06FF00'
	theme_setter = RecursiveKeyWordSetter()
	theme_setter.set_config(tk.Scale, bg=highlight, troughcolor=mid, highlightthickness=1, highlightbackground='#526D82')
	theme_setter.set_config(tk.OptionMenu, bg=mid, fg=text, activeforeground=text, activebackground='#404040')
	theme_setter.set_config(tk.Button, bg=mid, fg=text, activeforeground=text, activebackground='#404040')
	theme_setter.set_config(tk.Menu, bg=mid, fg=text, activeforeground=text, activebackground='#404040')
	theme_setter.set_config(tk.Entry, bg=mid, fg=text, disabledbackground=dark)
	theme_setter.set_config(tk.Label, bg=mid, fg=text)
	theme_setter.set_config(tk.Canvas, bg=mid)
	theme_setter.set_config(tk.Frame, bg=mid)
	theme_setter.set_config(TransversePlotsWidget, bg=mid, fg='#526D82', marker_color=highlight)
	theme_setter.apply_configs(root)

	bind_setter = RecursiveBindSetter()
	bind_setter.set_bind(tk.Button, '<Enter>', lambda widget: widget.configure(bg='#404040'))
	bind_setter.set_bind(tk.Entry, '<Enter>', lambda widget: widget.configure(bg='#404040'))
	bind_setter.set_bind(tk.Button, '<Leave>', lambda widget: widget.configure(bg=mid))
	bind_setter.set_bind(tk.Entry, '<Leave>', lambda widget: widget.configure(bg=mid))
	bind_setter.apply_binds(root)
	bind_setter.clear_binds()
	root.mainloop()