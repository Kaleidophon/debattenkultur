# -*- coding: utf-8 -*-

"""
Model for a parliament transcript of the German Bundestag.
"""

# PROJECT
from models.model import Model


class Transcript(Model):
    """
    Model for a parliament transcript of the German Bundestag.
    """
    def __init__(self, **init_attributes):
        formatting_functions = {"date": self._format_date}
        not_writable = {
            "title", "date", "location", "identifier", "president", "meps"
        }
        super(Transcript, self).__init__(
            formatting_functions=formatting_functions,
            non_writable=not_writable,
            **init_attributes
        )

    def _format_date(self, raw_date):
        # TODO: Implement
        pass
