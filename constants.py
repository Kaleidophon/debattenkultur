# -*- coding: utf-8 -*-

"""
Defining constants throughout the projects.
"""

# PROJECT
from parsing.parser import (
    HeaderParser,
    AgendaItemsParser,
    SessionHeaderParser,
    DiscussionsParser,
    AttachmentsParser
)

# Defining the map from section to their corresponding parsers
SECTIONS_TO_PARSERS = {
    "HEADER": HeaderParser,
    "AGENDA_ITEMS": AgendaItemsParser,
    "SESSION_HEADER": SessionHeaderParser,
    "DISCUSSIONS": DiscussionsParser,
    "ATTACHMENTS": AttachmentsParser
}
