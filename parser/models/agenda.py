# -*- coding: utf-8 -*-

"""
Model for an item of the agenda of the meeting.
"""

# PROJECT
from models.model import ParserTarget, RuleTarget


class Agenda(ParserTarget):
    """
    Model to group multiple agenda items into an agenda.
    """
    items = []

    def __init__(self, items):
        super().__init__(items=items)

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}


class AgendaItem(RuleTarget):
    """
    Model for an agenda item on the agenda of the German Bundestag's proceeding.
    """
    item_type = None
    number = None
    speakers = []
    subitems = []

    def __init__(self, header, contents):
        super().__init__(
            item_type=header,
            item_number=header,
            subitems=contents,
            formatting_functions={
                "item_type": self._get_agenda_item_type,
                "item_number": self._get_agenda_item_number,
                "subitems": self._split_agenda_subitems
            }
        )

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}

    def _get_agenda_item_type(self, header):
        # TODO (Implement) [DU 15.04.17]
        pass

    def _get_agenda_item_type(self, header):
        # TODO (Implement) [DU 15.04.17]
        pass

    def _split_agenda_subitems(self, subitems):
        # TODO (Implement) [DU 15.04.17]
        pass


class AgendaComment(RuleTarget):
    """
    Model for comments about the protocol's agenda.
    """
    comment = None
    identifier = None

    def __init__(self, contents):
        super().__init__(
            identifier=contents[0],
            comment=contents[1]
        )

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}


class AgendaAttachment(RuleTarget):
    """
    Model for attachments to the protocol's agenda.
    """
    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}


class AgendaContent(RuleTarget):
    """
    Superclass for the different kind of things bundled up in an agenda item.
    """
    originator = None
    content = None

    def __init__(self, originator, content):
        super().__init__(
            originator=originator, content=content
        )

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}


class Speech(AgendaContent):
    """
    Model for a speech in parliament.
    """
    def __init__(self, originator, content):
        super().__init__(originator, content)

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}


class Action(AgendaContent):
    """
    Model for any action which is not a speech or an introduction.
    """
    def __init__(self, originator, content, action_type):
        self.type = action_type
        super().__init__(originator, content)

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}


class Introduction(AgendaContent):
    """
    Model for an introduction at the beginning of an agenda item.
    """
    def __init__(self, originator, content):
        super().__init__(originator, content)

    @property
    def schema(self):
        # TODO (Implement) [DU 15.04.17]
        return {}
