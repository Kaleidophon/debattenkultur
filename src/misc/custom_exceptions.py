# -*- coding: utf-8 -*-

"""
Custom built exception for specific purposes.
"""


class CustomException(Exception):
    """
    Simple class to identify custom made exceptions.
    """
    def __init__(self, message):
        super(CustomException, self).__init__(message)


class NotWritableException(CustomException):
    """
    Exception that is raised when there is an attempt to overwrite a
    protected model attribute.
    """
    def __init__(self, attribute_name):
        msg = u"Attribute {} is not writable.".format(attribute_name)
        super(NotWritableException, self).__init__(msg)


class NotReadableException(CustomException):
    """
    Exception that is raised when there is an attempt to read a secret model
    attribute.
    """
    def __init__(self, attribute_name):
        msg = u"Attribute {} is not readable.".format(attribute_name)
        super(NotReadableException, self).__init__(msg)


class ProtocolParserAssignmentException(CustomException):
    """
    Exception that is raised when an unambiguous assignment of sub-parsers to
    protocol blocks wasn't possible.
    """
    def __init__(self, message):
        super(ProtocolParserAssignmentException, self).__init__(message)


class RuleApplicationException(CustomException):
    """
    Exception that is raised when the application of a parsing rule to its
    input failed.
    """
    def __init__(self, rule_name, rule_input, reason):
        super(RuleApplicationException, self).__init__(
            u"Rule {} couldn't be applied to the following input:\n\t{}\nThe "
            u"following problem occurred:{}\n".format(
                rule_name, rule_input, unicode(reason)
            )
        )


class ParserCoherenceException(CustomException):
    """
    Exception that is raised when a parser was initialized with illogical
    arguments.
    """
    def __init__(self, message):
        super(ParserCoherenceException, self).__init__(message)