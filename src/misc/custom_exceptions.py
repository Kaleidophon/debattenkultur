# -*- coding: utf-8 -*-

"""
Custom built exception for specific purposes.
"""
# TODO: Add documentation


class CustomException(Exception):
    """
    Simple class to identify custom made exceptions.
    """
    def __init__(self, message):
        super(CustomException, self).__init__(message)


class NotWritableException(CustomException):
    def __init__(self, attribute_name):
        msg = u"Attribute {} is not writable.".format(attribute_name)
        super(NotWritableException, self).__init__(msg)


class NotReadableException(CustomException):
    def __init__(self, attribute_name):
        msg = u"Attribute {} is not readable.".format(attribute_name)
        super(NotReadableException, self).__init__(msg)


class ProtocolParsingException(CustomException):

    def __init__(self, message):
        super(ProtocolParsingException, self).__init__(message)


class RuleApplicationException(CustomException):
    def __init__(self, rule_name, rule_input, reason):
        super(RuleApplicationException, self).__init__(
            u"Rule {} couldn't be applied to the following input:\n\t{}\nThe "
            u"following problem occurred:{}\n".format(
                rule_name, rule_input, unicode(reason)
            )
        )


class ParsingException(CustomException):

    def __init__(self, message):
        super(ParsingException, self).__init__(message)