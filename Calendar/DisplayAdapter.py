class DisplayAdapter (object):
	"""Interface for CalendarDesign output channels"""
	def render (self, design):
		raise NotImplementedError("Functions needs to be implemented")

	def calibrate (self):
		raise NotImplementedError("Functions needs to be implemented")