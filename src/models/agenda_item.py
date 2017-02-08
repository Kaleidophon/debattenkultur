# -*- coding: utf-8 -*-

"""
Model for an item of the agenda of the meeting.
"""

# PROJECT
from models.model import Model


class AgendaItem(Model):
    """
    Model for an agenda item on the agenda of the German Bundestag's proceeding.
    """
    meta = {}
    contents = []

    def __init__(self, meta, contents):
        super(AgendaItem, self).__init__(meta=meta, contents=contents)


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
