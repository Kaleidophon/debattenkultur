# -*- coding: utf-8 -*-

"""
Model superclass.
"""

# STD
from abc import ABCMeta

# PROJECT
from misc.helpers import NotWritableException, NotReadableException


class Model(object):
    __metaclass__ = ABCMeta
    formatting_functions = {}
    internals = {
        "formatting_functions", "internals", "not_writable", "not_readable"
    }
    not_writable = set()
    not_readable = set()

    def __init__(self, formatting_functions={}, internals=set(),
                 not_writable=set(), not_readable=set(), **init_attributes):
        self.formatting_functions.update(formatting_functions)
        self.internals = self.internals.union(internals)

        for attribute, value in init_attributes.iteritems():
            setattr(self, attribute, value)

        self.not_writable = self.not_writable.union(not_writable)
        self.not_readable = self.not_readable.union(not_readable)

    def __setattr__(self, key, value):
        if key in self.not_writable:
            raise NotWritableException(key)

        if key in self.formatting_functions:
            value = self.formatting_functions[key](value)

        super(Model, self).__setattr__(key, value)

    def __getattr__(self, item):
        if item in self.not_readable:
            raise NotReadableException(item)
        return super(Model, self).__getattribute__(item)
