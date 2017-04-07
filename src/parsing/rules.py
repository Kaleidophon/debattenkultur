# -*- coding: utf-8 -*-

"""
Parsing rules used to parse the documents.
"""

# STD
import re

# PROJECT
from config import (
    PROTOCOL_AGENDA_ITEM_PATTERN,
    PROTOCOL_AGENDA_ATTACHMENT_PATTERN
)
from models.header import Header
from models.model import Filler
from models.agenda_item import (
    AgendaItem,
    Agenda,
    AgendaAttachment,
    AgendaComment
)
from misc.custom_exceptions import RuleApplicationException


class RuleTrigger(object):
    trigger_regex = None

    def __init__(self, trigger_regex):
        self.trigger_regex = trigger_regex

    def check(self, line):
        return re.match(self.trigger_regex, line) is not None


class Rule(object):
    """
    Superclass for parsing rules.
    """
    rule_input = None
    rule_target = None
    rule_trigger = None

    def __init__(self, rule_input, rule_target, rule_trigger):
        self.rule_input = rule_input
        self.rule_target = rule_target
        self.rule_trigger = rule_trigger

    def apply(self):
        """
        Apply this rule to the rules input. Rule inputs can be
        document lines.
        """
        try:
            self.prepare_rule_input()
            return self.rule_target(self.rule_input)
        except Exception as e:
            self._application_failed(e)

    def _application_failed(self, reason):
        """
        Raise error if the application of the rule failed.
        """
        raise RuleApplicationException(
            self.__class__.__name__, self.rule_input, reason
        )

    def triggers(self):
        return self.rule_trigger.check(self.rule_input)

    def expand(self, fillers):
        """
        Expand a rule's input by one or more fillers.
        """
        # Convert to iterable if it's just a single filler
        if type(fillers) not in (set, list, tuple):
            fillers = [fillers]

        assert all([isinstance(filler, Filler) for filler in fillers])

        self.rule_input.extend(fillers)
        return self.rule_target(self.rule_input)

    def prepare_rule_input(self):
        self.rule_input = [
            getattr(input_element, "line") for input_element in self.rule_input
        ]


class HeaderRule(Rule):
    """
    Single easy rule to parse the protocol header in one go.
    """
    def __init__(self, rule_input):
        super(HeaderRule, self).__init__(rule_input, Header)

    def apply(self):
        if len(self.rule_input) == 4:
            return self.rule_target(
                parliament=self.rule_input[0],
                document_type=self.rule_input[1],
                number=self.rule_input[2],
                location=self.rule_input[3],
                date=self.rule_input[3]
            )
        else:
            self._application_failed()


class AgendaItemRule(Rule):
    """
    Rule to parse AgendaItems.
    """
    def __init__(self, rule_input):
        super(AgendaItemRule, self).__init__(rule_input, AgendaItem)


class AgendaCommentRule(Rule):
    """
    Rule to parse a comment to the agenda.
    """
    def __init__(self, rule_input):
        super(AgendaCommentRule, self).__init__(rule_input, AgendaComment)

    def apply(self):
        if not len(self.rule_input) > 2:
            self._application_failed(
                u"Rule input is too big ({} found, 1 expected".format(
                    len(self.rule_input)
                )
            )

        if self._doesnt_match_any_agenda_pattern(self.rule_input[0]) and \
                self._doesnt_match_any_agenda_pattern(self.rule_input[1]):
            return self.rule_target(
                contents=self.rule_input
            )
        else:
            self._application_failed()

    # TODO: Refactor
    def _doesnt_match_any_agenda_pattern(self, input_element):
        return not self._element_matches_pattern(
            PROTOCOL_AGENDA_ITEM_PATTERN, input_element
        ) and not self._element_matches_pattern(
            PROTOCOL_AGENDA_ATTACHMENT_PATTERN, input_element
        )


class AgendaAttachmentRule(Rule):
    """
    Rule to parse Attachments to the Agenda.
    """
    def __init__(self, rule_input):
        super(AgendaAttachmentRule, self).__init__(
            rule_input,
            AgendaAttachment
        )


class AgendaRule(Rule):
    """
    Rule to group multiple agenda items to an agenda.
    """
    def __init__(self, rule_input):
        super(AgendaRule, self).__init__(rule_input, Agenda)
