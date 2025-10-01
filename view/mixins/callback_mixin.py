from typing import Callable


#manages a resgistry  {'callback_name': callback_function} 
class CallbackMixin:
	def __init__(self, *args, **kwargs):
		self._callback_registry: dict[str, Callable] = {}
		super().__init__(*args, **kwargs)

	def register_callback_name(self, callback_name):
		self._callback_registry.setdefault(callback_name, None)

	def set_callback_function(self, callback_name, callback_func):
		if callback_name not in self._callback_registry:
			raise KeyError(f'{callback_name} has not been registered.')
		self._callback_registry[callback_name] = callback_func

	def _execute_callback(self, callback_name, *args, **kwargs):
		if callback_name not in self._callback_registry: #Check that the callback is registered
			raise KeyError(f"Callback name '{callback_name}' has not been registered.")
		callback_function = self._callback_registry[callback_name]

		if not callback_function: #Check that the callback has associated functions
			raise ValueError(f"callback function for '{callback_name}' has not been set.")

		callback_function(*args, **kwargs)
