#!/usr/bin/python3
# -*- coding: utf-8 -*-
class DisplayAdapter (object):
	"""Interface for CalendarDesign output channels"""
	def render ():
		raise NotImplementedError("Functions needs to be implemented")

	def calibrate ():
		raise NotImplementedError("Functions needs to be implemented")

	def sleep ():
		raise NotImplementedError("Functions needs to be implemented")