import tkinter as tk
from ..custom_widgets.base_frame import BaseFrame


'''TabsWidget builds a BaseFrame packed with tkinter buttons named according to tab_names.'''
'''On click, a tab button will raise all tab_buttons, then sink itself.'''
'''On click, a tab button will execute all functions registered to 'on_tab_change' in the callback registry with the string argument button_name.'''

class Tabs(BaseFrame):
	def __init__(self, parent, tab_names: list[str], **kwargs):
		super().__init__(parent, **kwargs)
		self.tab_buttons = {}
		self.register_callback_name('on_tab_clicked') #associated function must take button_name (string) as its only argument.
		self.set_tab_names(tab_names)

		# #Dynamically create buttons from tab_names and add them to a dictionary
		# #All buttons share the same callback function. Each button passes its specific name to the callback when clicked.
		# for button_name in self.tab_names:
		# 	button = tk.Button(self, text=button_name, command=lambda n=button_name: [self.sink_selected_tab(n), self._execute_callback('on_tab_clicked', n)])
		# 	self.tab_buttons[button_name] = button
		# 	button.pack(side='left', expand=True, fill='x')

	def set_tab_names(self, tab_names):
		for button in self.tab_buttons.values():
			button.destroy()
		self.tab_buttons.clear()

		#Dynamically create buttons from tab_names and add them to a dictionary
		#All buttons share the same callback function. Each button passes its specific name to the callback when clicked.
		for button_name in tab_names:
			button = tk.Button(self, text=button_name, command=lambda n=button_name: [self.sink_selected_tab(n), self._execute_callback('on_tab_clicked', n)])
			self.tab_buttons[button_name] = button
			button.pack(side='left', expand=True, fill='x')


	#raise all tab buttons, then sink a specified button. Called whenever a tab button is clicked.
	def sink_selected_tab(self, button):
		for _ in self.tab_buttons.values():
			_.configure(relief='raised')
		self.tab_buttons[button].configure(relief='sunken')