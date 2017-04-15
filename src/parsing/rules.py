# -*- coding: utf-8 -*-

"""
Parsing rules used to parse the documents.
"""

# STD
import abc
import re

# PROJECT
from config import HEADER_RULE_TRIGGER
from models.header import HeaderInformation
from models.model import Filler
from models.agenda_item import (
    AgendaItem,
    Agenda,
    AgendaAttachment,
    AgendaComment
)
from misc.custom_exceptions import RuleApplicationException


class RuleTrigger:
    """
    Rule triggers will "anchor" a rule at a certain line in case the
    trigger's regex matches the current line. Afterwards, the rule will
    expand over all filler lines.
    """
    trigger_regex = None

    def __init__(self, trigger_regex):
        self.trigger_regex = trigger_regex

    def check(self, line):
        return re.search(self.trigger_regex, line) is not None


class Rule:
    """
    Superclass for parsing rules.
    """
    rule_input = None
    rule_target_class = None
    rule_trigger = None

    def __init__(self, rule_input, rule_target_class, trigger_regex):
        self.rule_input = rule_input
        self.rule_target_class = rule_target_class
        self.rule_trigger = RuleTrigger(trigger_regex)

    def apply(self):
        """
        Apply this rule to the rules input. Rule inputs can be
        document lines.
        """
        try:
            self.prepare_rule_input()
            return self.rule_target
        except Exception as e:
            self._application_failed(e)

    @abc.abstractproperty
    def rule_target(self):
        """
        Return the rule target with custom key word arguments.
        """
        return self.rule_target_class(input=self.rule_input)

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

        if type(self.rule_input) != list:
            self.rule_input = [self.rule_input]

        self.rule_input.extend(fillers)

    def prepare_rule_input(self):
        self.rule_input = [
            getattr(input_element, "line")
            if isinstance(input_element, Filler) else input_element
            for input_element in self.rule_input
        ]


class HeaderRule(Rule):
    """
    Single easy rule to parse the protocol header in one go.
    """
    def __init__(self, rule_input):
        super().__init__(rule_input, HeaderInformation, HEADER_RULE_TRIGGER)

    @property
    def rule_target(self):
        return self.rule_target_class(
            parliament=self.rule_input[0],
            document_type=self.rule_input[1],
            number=self.rule_input[2],
            location=self.rule_input[3],
            date=self.rule_input[3]
        )


class AgendaItemRule(Rule):
    """
    Rule to parse AgendaItems.
    """
    def __init__(self, rule_input):
        # TODO (Refactor): Add rule trigger
        super().__init__(rule_input, AgendaItem, "")

    @property
    def rule_target(self):
        # TODO (Implement): [DU 15.04.17]
        return {}


class AgendaCommentRule(Rule):
    """
    Rule to parse a comment to the agenda.
    """
    def __init__(self, rule_input):
        # TODO (Refactor): Add rule trigger
        super().__init__(rule_input, AgendaComment, "")

    @property
    def rule_target(self):
        return self.rule_target_class(
            contents=self.rule_input
        )


class AgendaAttachmentRule(Rule):
    """
    Rule to parse Attachments to the Agenda.
    """
    def __init__(self, rule_input):
        # TODO (Refactor): Add rule trigger
        super().__init__(
            rule_input,
            AgendaAttachment,
            ""
        )

    @property
    def rule_target(self):
        # TODO (Implement): [DU 15.04.17]
        return {}


class AgendaRule(Rule):
    """
    Rule to group multiple agenda items to an agenda.
    """
    def __init__(self, rule_input):
        # TODO (Refactor): Add rule trigger
        super().__init__(rule_input, Agenda, "")

    @property
    def rule_target(self):
        # TODO (Implement): [DU 15.04.17]
        return {}
