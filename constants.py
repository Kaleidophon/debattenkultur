# -*- coding: utf-8 -*-

"""
Defining constants throughout the projects.
"""

# PROJECT
from parsing.parser import (
	HeaderParser,
	AgendaParser,
	SessionHeaderParser,
	SessionParser,
	AttachmentsParser
)

# Defining the map from section to their corresponding parsers
SECTIONS_TO_PARSERS = {
    "HEADER": HeaderParser,
    "AGENDA_ITEMS": AgendaParser,
    "SESSION_HEADER": SessionHeaderParser,
    "DISCUSSIONS": SessionParser,
    "ATTACHMENTS": AttachmentsParser
}
