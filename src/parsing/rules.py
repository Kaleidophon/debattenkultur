# -*- coding: utf-8 -*-

"""
Parsing rules used to parse the documents.
"""

# STD
from abc import abstractmethod
import re
from collections import namedtuple

# PROJECT
from config import PROTOCOL_AGENDA_ITEM_PATTERN
from models.header import Header
from models.agenda_item import AgendaItem, Agenda
from misc.custom_exceptions import RuleApplicationException

# Create type of named tuple to increase readability
RuleResult = namedtuple("RuleResult", "rule_target skip_lines")


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
        raise RuleApplicationException(
            self.__class__.__name__, self.rule_input
        )


class HeaderRule(Rule):
    """
    Single easy rule to parse the protocol header in one go.
    """
    def __init__(self, rule_input):
        super(HeaderRule, self).__init__(rule_input, Header)

    def apply(self):
        if len(self.rule_input) == 4:
            # TODO: Make return namedtuple for readability
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
            raise RuleApplicationException(
                self.__class__.__name__, self.rule_input
            )


class AgendaItemRule(Rule):
    """
    Rule to parse AgendaItems.
    """
    def __init__(self, rule_input):
        super(AgendaItemRule, self).__init__(rule_input, AgendaItem)

    def apply(self):
        ai_pattern = PROTOCOL_AGENDA_ITEM_PATTERN
        current_ai = []

        for index, line in enumerate(self.rule_input):
            if isinstance(line, str) or isinstance(line, unicode):
                if re.match(ai_pattern, line):
                    current_ai.append(line)
                    for ai_index in range(index+1, len(self.rule_input)):
                        ai_line = self.rule_input[ai_index]
                        if re.match(ai_pattern, ai_line):
                            return RuleResult(
                                rule_target=self.rule_target(
                                    header=current_ai[0],
                                    contents=current_ai
                                ),
                                skip_lines=len(current_ai)
                            )
                        current_ai.append(ai_line)
            else:
                raise RuleApplicationException(
                    self.__class__.__name__, self.rule_input
                )

        raise RuleApplicationException(
            self.__class__.__name__, self.rule_input
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
                raise RuleApplicationException(
                    self.__class__.__name__, self.rule_input
                )

        return RuleResult(
            rule_target=self.rule_target(self.rule_input),
            skip_lines=len(self.rule_input)
        )
