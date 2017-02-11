# -*- coding: utf-8 -*-

"""
Parsing rules used to parse the documents.
"""


class Rule(object):

    def __init__(self, rule_input, rule_target):
        self.rule_input = rule_input
        self.rule_target = rule_target
