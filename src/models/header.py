# -*- coding: utf-8 -*-

"""
Header model.
"""

# STD
from datetime import datetime
import locale

# PROJECT
from models.model import Model
from config import PROTOCOL_DATE_FORMAT


class Header(Model):

    def __init__(self, **init_args):
        super().__init__(
            not_writable={
                "parliament", "document_type", "number", "location", "date"
            },
            formatting_functions={
                "location": self._extract_location,
                "date": self._extract_date
            },
            **init_args
        )

    @staticmethod
    def _extract_date(raw_line):
        loc = locale.setlocale(locale.LC_TIME, "de_DE")
        raw_date = ",".join(raw_line.split(",")[1:]).strip()
        datetime_object = datetime.strptime(raw_date, PROTOCOL_DATE_FORMAT)
        return datetime_object

    @staticmethod
    def _extract_location(raw_line):
        return raw_line.split(",")[0]
