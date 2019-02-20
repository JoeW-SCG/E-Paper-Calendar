class DisplayAdapter (object):
	"""Interface for CalendarDesign output channels.
    Needs implementation of width and height properties."""
	def render (self, design):
		raise NotImplementedError("Functions needs to be implemented")

	def calibrate (self):
		raise NotImplementedError("Functions needs to be implemented")