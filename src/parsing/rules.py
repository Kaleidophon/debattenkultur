# -*- coding: utf-8 -*-

"""
Parsing rules used to parse the documents.
"""

# STD
from abc import abstractmethod

# PROJECT
from models.header import Header
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
        """
        pass


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
            raise RuleApplicationException(
                self.__class__.__name__, self.rule_input
            )
