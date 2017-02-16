# -*- coding: utf-8 -*-

"""
Parsing rules used to parse the documents.
"""

# STD
from abc import abstractmethod
import re

# PROJECT
from models.header import Header
from models.agenda_item import AgendaItem
from misc.helpers import RuleApplicationException


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
            return self.rule_target(
                parliament=self.rule_input[0],
                document_type=self.rule_input[1],
                number=self.rule_input[2],
                location=self.rule_input[3],
                date=self.rule_input[3]
            ), 4
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
        ai_pattern = r"(Zusatzt|T)agesordnungspunkt \d+:"
        current_ai = []
        iter_input = iter(enumerate(self.rule_input))

        for index, line in iter_input:
            if isinstance(line, str) or isinstance(line, unicode):
                if re.match(ai_pattern, line):
                    current_ai.append(line)
                    for ai_index in range(index+1, len(self.rule_input)):
                        ai_line = self.rule_input[ai_index]
                        if re.match(ai_pattern, ai_line):
                            # TODO: Put data into model
                            # TODO: Make return namedtuple for readability
                            print current_ai
                            return current_ai, len(current_ai)
                        current_ai.append(ai_line)

        raise RuleApplicationException(
            self.__class__.__name__, self.rule_input
        )





