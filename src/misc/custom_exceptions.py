# -*- coding: utf-8 -*-

"""
Custom built exception for specific purposes.
"""


class CustomException(Exception):
    """
    Simple class to identify custom made exceptions.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotWritableException(CustomException):
    """
    Exception that is raised when there is an attempt to overwrite a
    protected model attribute.
    """
    def __init__(self, attribute_name):
        self.message = "Attribute {} is not writable.".format(attribute_name)
        super().__init__(self.message)


class NotReadableException(CustomException):
    """
    Exception that is raised when there is an attempt to read a secret model
    attribute.
    """
    def __init__(self, attribute_name):
        self.message = "Attribute {} is not readable.".format(attribute_name)
        super().__init__(self.message)


class ProtocolParserAssignmentException(CustomException):
    """
    Exception that is raised when an unambiguous assignment of sub-parsers to
    protocol blocks wasn't possible.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class RuleApplicationException(CustomException):
    """
    Exception that is raised when the application of a parsing rule to its
    input failed.
    """
    def __init__(self, rule_name, rule_input, reason):
        self.message = (
            "Rule {} couldn't be applied to the following input:\n\t{}\nThe "
            "following problem occurred:{}\n".format(
                rule_name, rule_input, reason
            )
        )
        super().__init__(self.message)


class ParserCoherenceException(CustomException):
    """
    Exception that is raised when a parser was initialized with illogical
    arguments.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)
