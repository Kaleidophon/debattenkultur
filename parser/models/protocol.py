# -*- coding: utf-8 -*-

"""
Model for the whole protocol, bundling up all the models representing
subsections.
"""

# PROJECT
from models.model import ParserTarget


class Protocol(ParserTarget):
    """
    Global model to contain all other models.
    """
    items = []

    def __init__(self, items):
        super().__init__(items=items)

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}
