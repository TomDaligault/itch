from typing import Callable


#Used to add new keywords to the configure method for tkinter widget subclasses via a registry
#Can be used to override functionality for existing keywords as well.
#Allows for tkinter style usage widget.configure(key=value)
class ConfigureMixin:
	_configure_registry: dict[str, Callable] = {} #map keywords to methods in the subclass
	
	def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)

	#check if key is in _custom_configure_registry
	#grab and execute whatever method is associated with key in _custom_configure_registry
	#remove custom keywords and delegate to the superclass configure
	def configure(self, **kwargs):
		for key, value, in list(kwargs.items()):
			if key in self._configure_registry:
				handler = self._configure_registry[key]
				handler(value)
				kwargs.pop(key)

		#if a standard tk configure kwarg is registered, it will NOT be passed to super().configure(), write the handler accordingly
		super().configure(**kwargs)