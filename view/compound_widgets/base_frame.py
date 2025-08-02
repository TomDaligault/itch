import tkinter as tk
from typing import Callable


'''CompoundWidgets are extensions of tkinter Frame that come pre-loaded with widgets.'''
'''All custom frames inherit from a base class with methods for toggling widget state and visibility.'''
'''All widgets placed inside of any CompoundWidget must be placed using .grid(**kwargs).'''
'''Commands are supported via optionally providing a callback registry.'''
'''Widgets in frames will check the registry for their assigned callback_name and execute all associated functions'''
'''I am told that this registry acts like an event bus. Will consider seperating developing a seperate module for this.'''

#Considering changing callback_names formatting to match tkinter events.
#Should add a list of expected callback_names somewhere
class BaseFrame(tk.Frame):
	def __init__(self, parent: tk.Frame, callback_registry: dict[str, list[Callable]] = None, **kwargs):
		super().__init__(parent, **kwargs)
		self.callback_registry = callback_registry or {}

	def _execute_callback(self, callback_name, *args, **kwargs):
		if not self.callback_registry: #Check that the registry is not empty
			raise ValueError(f"Callback registry is empty, please provide a callback registry.")

		if callback_name not in self.callback_registry: #Check that the callback is registered
			raise KeyError(f"Callback name '{callback_name}' not found in registry.")

		callback_functions = self.callback_registry[callback_name]

		if not callback_functions: #Check that the callback has associated functions
			raise ValueError(f"Callback name '{callback_name}' has no associated functions")

		for function in callback_functions: #execute all associated functions 
			function(*args, **kwargs)

	def show_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.grid()
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def hide_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.grid_remove()
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def enable_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.configure(state='normal')
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def disable_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if isinstance(widget, tk.Widget):
			widget.configure(state='disabled')
		else:
			raise ValueError(f"No widget named '{widget_name}'")

	def enable_all_widgets(self):
		for widget in self.winfo_children():
			try: 
				widget.configure(state='normal')
			except (tk.TclError, TypeError):
				pass # Widget may not support 'state'; skip it

	def disable_all_widgets(self):
		for widget in self.winfo_children():
			try: 
				widget.configure(state='disabled')
			except (tk.TclError, TypeError):
				pass # Widget may not support 'state'; skip it