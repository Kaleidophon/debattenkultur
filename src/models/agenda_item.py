# -*- coding: utf-8 -*-

"""
Model for an item of the agenda of the meeting.
"""

# STD
import re

# PROJECT
from config import (
    PROTOCOL_AGENDA_ITEM_PATTERN,
    PROTOCOL_AGENDA_SUBITEM_PATTERN,
    PROTOCOL_AGENDA_SUBITEM_ITEMTYPE
)
from models.model import Model


class Agenda(Model):
    """
    Model to group multiple agenda items into an agenda.
    """
    items = []

    def __init__(self, items):
        super(Agenda, self).__init__(items=items)


class AgendaItem(Model):
    """
    Model for an agenda item on the agenda of the German Bundestag's proceeding.
    """
    item_type = None
    number = None
    speakers = []
    subitems = []

    def __init__(self, header, contents):
        super(AgendaItem, self).__init__(
            item_type=header,
            item_number=header,
            subitems=contents,
            formatting_functions={
                "item_type": self._get_agenda_item_type,
                "item_number": self._get_agenda_item_number,
                "subitems": self._split_agenda_subitems
            }
        )

    @staticmethod
    def _get_agenda_item_type(header):
        if re.match(PROTOCOL_AGENDA_ITEM_PATTERN, header):
            return header.replace(":", "").split(" ")[0]
        elif re.match(PROTOCOL_AGENDA_SUBITEM_PATTERN, header):
            return PROTOCOL_AGENDA_SUBITEM_ITEMTYPE

    @staticmethod
    def _get_agenda_item_number(header):
        if re.match(PROTOCOL_AGENDA_ITEM_PATTERN, header):
            return int(header.replace(":", "").split(" ")[1])
        elif re.match(PROTOCOL_AGENDA_SUBITEM_PATTERN, header):
            return header.split("\t")[0].replace(")", "").upper()

    @staticmethod
    def _split_agenda_subitems(contents):
        contents.pop(0)  # Remove header
        subitems = []
        current_subitem = []

        for line in contents:
            if re.match(PROTOCOL_AGENDA_SUBITEM_PATTERN, line):
                if current_subitem:
                    subitems.append(
                        AgendaItem(
                            header=current_subitem[0],
                            contents=current_subitem
                        )
                    )
                current_subitem = [line]
            else:
                current_subitem.append(line)

        if len(subitems) == 0:
            subitems = contents

        return subitems


class AgendaComment(Model):
    """
    Model for comments about the protocol's agenda.
    """
    comment = None
    identifier = None

    def __init__(self, contents):
        super(AgendaComment, self).__init__(
            identifier=contents[0],
            comment=contents[1]
        )


class AgendaAttachment(Model):
    """
    Model for attachments to the protocol's agenda.
    """
    pass


class AgendaContent(Model):
    """
    Superclass for the different kind of things bundled up in an agenda item.
    """
    originator = None
    content = None

    def __init__(self, originator, content):
        super(AgendaContent, self).__init__(
            originator=originator, content=content
        )


class Speech(AgendaContent):
    """
    Model for a speech in parliament.
    """
    def __init__(self, originator, content):
        super(Speech, self).__init__(originator, content)


class Action(AgendaContent):
    """
    Model for any action which is not a speech or an introduction.
    """
    def __init__(self, originator, content, action_type):
        self.type = action_type
        super(Action, self).__init__(originator, content)


class Introduction(AgendaContent):
    """
    Model for an introduction at the beginning of an agenda item.
    """
    def __init__(self, originator, content):
        super(Introduction, self).__init__(originator, content)
