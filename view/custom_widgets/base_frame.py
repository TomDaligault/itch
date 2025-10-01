import tkinter as tk
from typing import Callable

from ..mixins import CallbackMixin, ConfigureMixin



'''CompoundWidgets are extensions of tkinter Frame that come pre-loaded with widgets.'''
'''All custom frames inherit from a base class with methods for toggling widget state and visibility.'''
'''All widgets placed inside of any CompoundWidget must be placed using .grid(**kwargs).'''
class BaseFrame(ConfigureMixin, CallbackMixin, tk.Frame):
	def __init__(self, parent: tk.Frame, **kwargs):
		super().__init__(parent, **kwargs)

	def show_widget(self, widget_name):
		self._get_widget(widget_name).grid()

	def hide_widget(self, widget_name):
		self._get_widget(widget_name).grid_remove()

	def enable_widget(self, widget_name):
		self._get_widget(widget_name).configure(state='normal')

	def disable_widget(self, widget_name):
		self._get_widget(widget_name).configure(state='disabled')

	def enable_all_widgets(self):
		for widget in self.winfo_children():
			try: 
				widget.configure(state='normal')
			except (tk.TclError, TypeError):
				pass #silently handle widgets that do not support state

	def disable_all_widgets(self):
		for widget in self.winfo_children():
			try: 
				widget.configure(state='disabled')
			except (tk.TclError, TypeError):
				pass #silently handle widgets that do not support state

	def _get_widget(self, widget_name):
		widget = getattr(self, widget_name, None)
		if not isinstance(widget, tk.Widget):
			raise ValueError(f"No widget named '{widget_name}'")

		return widget