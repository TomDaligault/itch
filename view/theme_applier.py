import tkinter as tk
'''
RecursiveKeyWordSetter is used to recursively configure keywords for full widget child-trees.
Keeps an interal dictionary mapping tkinter widget classes to dictionaries of kwargs.
Users populate the map for each widget class individually, then apply all set configs to a widget (typically root) and all its children.
Individual mappings can be redefined, or the full map can be cleared, repopulated, and reapplied as desired.
Typical use-case is setting a consistent theme across an oldschool tk.Widget application.

Techincally supports keyword setting for custom tk widget subclasses with their own .configure() methods.
If a subclass and superclass are both mapped, then both config maps will by applied to instances of the subclass in the order that the maps were added.
This can lead to unexpected results if different values are assigned to the same keyword in different maps.
Subclass .configure() methods should be written with this in mind.
'''
class RecursiveKeyWordSetter:
	def __init__(self):
		self.class_config_map = {}

	def set_config(self, widget_class, **kwargs):
		self.class_config_map[widget_class] = kwargs

	def clear_configs(self):
		self.class_config_map = {}

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
'''
RecursiveBindSetter is used to recursively set bindings for full widget child-trees.
Keeps an interal dictionary mapping tkinter widget classes to dictionaries events and functions.
Users populate the map for each widget class individually, then apply all set bindings to a widget (typically root) and all its children.
Individual mappings can be redefined, or the full map can be cleared, repopulated, and reapplied as desired.

Techincally supports binding for custom tk widget subclasses with their own .bind() methods.
If a subclass and superclass are both mapped, then all bindings defined for both the subclass and superclass will be set on all subclass instances.
'''
class RecursiveBindSetter:
	def __init__(self):
		self.class_bind_map = {}

	def set_bind(self, widget_class, event, func):
		if widget_class not in self.class_bind_map:
			self.class_bind_map[widget_class] = {}
		self.class_bind_map[widget_class][event] = func

	def clear_binds(self):
		self.class_bind_map = {}

	def apply_binds(self, widget):
		for widget_class, bind_dict in self.class_bind_map.items(): #for all widget_class and binding specified in the map,
			if isinstance(widget, widget_class): #check if widget is an instance of a widget_class
				for event, func in bind_dict.items(): 
					widget.bind(event, lambda event, f=func: f(event.widget), add='+') #bind each event to each func

		for child in widget.winfo_children():
			self.apply_binds(child)