# -*- coding: utf-8 -*-

"""
Header model.
"""

# STD
import locale
from datetime import datetime

from config import PROTOCOL_DATE_FORMAT
from models.model import ParserTarget, RuleTarget


class Header(ParserTarget):

    def __init__(self, header_information):
        super().__init__(
            header_information=header_information[0]
        )

    @property
    def schema(self):
        return {
            "header_information": {
                "required": True,
                "type": "ruletarget"
            }
        }


class HeaderInformation(RuleTarget):
    def __init__(self, parliament, document_type, number, location, date):
        super().__init__(
            not_writable={
                "parliament", "document_type", "number", "location", "date"
            },
            formatting_functions={
                "location": self._extract_location,
                "date": self._extract_date
            },
            parliament=parliament,
            document_type=document_type,
            number=number,
            location=location,
            date=date
        )

    @property
    def schema(self):
        # TODO (Improve): Refactor with "allowed" property [DU 15.04.17]
        return {
            "parliament": {
                "required": True,
                "type": "string"
            },
            "document_type": {
                "required": True,
                "type": "string"
            },
            "number": {
                "required": True,
                "type": "string"
            },
            "location": {
                "required": True,
                "type": "string"
            },
            "date": {
                "required": True,
                "type": "string"
            }
        }

    @staticmethod
    def _extract_date(raw_line):
        loc = locale.setlocale(locale.LC_TIME, "de_DE")
        raw_date = ",".join(raw_line.split(",")[1:]).strip()
        datetime_object = datetime.strptime(raw_date, PROTOCOL_DATE_FORMAT)
        return datetime_object

    @staticmethod
    def _extract_location(raw_line):
        return raw_line.split(",")[0]

