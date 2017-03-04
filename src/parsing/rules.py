# -*- coding: utf-8 -*-

"""
Parsing rules used to parse the documents.
"""

# STD
from abc import abstractmethod
import re
from collections import namedtuple

# PROJECT
from config import (
    PROTOCOL_AGENDA_ITEM_PATTERN,
    PROTOCOL_AGENDA_ATTACHMENT_PATTERN
)
from models.model import Model
from models.header import Header
from models.agenda_item import (
    AgendaItem,
    Agenda,
    AgendaAttachment,
    AgendaComment
)
from misc.custom_exceptions import RuleApplicationException

# Create type of named tuple to increase readability
RuleResult = namedtuple("RuleResult", "rule_target skip_lines")


# TODO: Add rule "triggers"



class Rule(object):
    """
    Superclass for parsing rules.
    """
    def __init__(self, rule_input, rule_target):
        self.rule_input = rule_input
        self.rule_target = rule_target

    @abstractmethod
    def apply(self):
        """
        Apply this rule to the rules input. Rule inputs can be
        document lines / words or models.

        Rules return either a result or an exception of the application of
        the rule to the given input failed. The result is a namedtuple
        consisting in both the parsed data wrapped within a specific model (
        rule_target) and the number of lines the parser has to skip now (in
        case the rule worked with lookaheads).
        """
        self._application_failed()

    def _look_ahead_until_next_match(self, pattern, rule_input):
        """
        Make lookaheads until you encounter the next elements that matches
        the pattern. Otherwise return None.:
        """
        current_element = []

        for i, iline in enumerate(rule_input):
            if self._element_matches_pattern(pattern, iline) or \
                    self._is_parsed(iline):
                current_element.append(iline)
                for j in range(i + 1, len(rule_input)):
                    jline = rule_input[j]
                    if self._element_matches_pattern(pattern, jline) or \
                            self._is_parsed(jline):
                        return RuleResult(
                            rule_target=self.rule_target(
                                header=current_element[0],
                                contents=current_element
                            ),
                            skip_lines=len(current_element)
                        )
                    current_element.append(jline)
            else:
                break

        self._application_failed()

    def _application_failed(self):
        """
        Raise error if the application of the rule failed.
        """
        raise RuleApplicationException(
            self.__class__.__name__, self.rule_input
        )

    @staticmethod
    def _element_matches_pattern(pattern, input_element):
        if isinstance(input_element, str) or isinstance(input_element, unicode):
            return re.match(pattern, input_element)
        return False

    @staticmethod
    def _is_parsed(input_element):
        return isinstance(input_element, Model)


class HeaderRule(Rule):
    """
    Single easy rule to parse the protocol header in one go.
    """
    def __init__(self, rule_input):
        super(HeaderRule, self).__init__(rule_input, Header)

    def apply(self):
        if len(self.rule_input) == 4:
            return RuleResult(
                rule_target=self.rule_target(
                    parliament=self.rule_input[0],
                    document_type=self.rule_input[1],
                    number=self.rule_input[2],
                    location=self.rule_input[3],
                    date=self.rule_input[3]
                ),
                skip_lines=4
            )
        else:
            self._application_failed()


class AgendaItemRule(Rule):
    """
    Rule to parse AgendaItems.
    """
    def __init__(self, rule_input):
        super(AgendaItemRule, self).__init__(rule_input, AgendaItem)

    def apply(self):
        return self._look_ahead_until_next_match(
            PROTOCOL_AGENDA_ITEM_PATTERN,
            self.rule_input
        )


class AgendaCommentRule(Rule):
    """
    Rule to parse a comment to the agenda.
    """
    def __init__(self, rule_input):
        super(AgendaCommentRule, self).__init__(rule_input, AgendaComment)

    def apply(self):
        if not len(self.rule_input) > 2:
            self._application_failed()

        if self._doesnt_match_any_agenda_pattern(self.rule_input[0]) and \
                self._doesnt_match_any_agenda_pattern(self.rule_input[1]):
            return RuleResult(
                rule_target=self.rule_target(
                    contents=self.rule_input
                ),
                skip_lines=1
            )
        else:
            self._application_failed()

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

    def apply(self):
        return self._look_ahead_until_next_match(
            PROTOCOL_AGENDA_ATTACHMENT_PATTERN,
            self.rule_input
        )


class AgendaRule(Rule):
    """
    Rule to group multiple agenda items to an agenda.
    """
    def __init__(self, rule_input):
        super(AgendaRule, self).__init__(rule_input, Agenda)

    def apply(self):
        for inpt in self.rule_input:
            if not isinstance(inpt, AgendaItem):
                self._application_failed()

        return RuleResult(
            rule_target=self.rule_target(self.rule_input),
            skip_lines=len(self.rule_input)
        )
