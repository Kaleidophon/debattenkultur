# -*- coding: utf-8 -*-

"""
Helper functions and classes.
"""


class NotWritableException(Exception):
	def __init__(self, attribute_name):
		msg = u"Attribute {} is not writable.".format(attribute_name)
		super(NotWritableException, self).__init__(msg)


class NotReadableException(Exception):
	def __init__(self, attribute_name):
		msg = u"Attribute {} is not readable.".format(attribute_name)
		super(NotReadableException, self).__init__(msg)
