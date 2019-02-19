#!/usr/bin/python3
# -*- coding: utf-8 -*-
class DisplayAdapter (object):
	"""Interface for CalendarDesign output channels"""
	def render (self, design):
		raise NotImplementedError("Functions needs to be implemented")

	def calibrate (self):
		raise NotImplementedError("Functions needs to be implemented")

	def sleep (self):
		raise NotImplementedError("Functions needs to be implemented")