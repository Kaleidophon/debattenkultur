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

    def __init__(self, lines):
        super(Header, self).__init__(
            not_writable={
                "parliament", "document_type", "number", "location", "date"
            },
            formatting_functions={
                "location": self._extract_location,
                "date": self._extract_date
            },
            parliament=lines[0], document_type=lines[1], number=lines[2],
            location=lines[3], date=lines[3]
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
