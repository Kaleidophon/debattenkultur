# -*- coding: utf-8 -*-

"""
Helper functions and classes.
"""

# STD
import types


class NotWritableException(Exception):
    def __init__(self, attribute_name):
        msg = u"Attribute {} is not writable.".format(attribute_name)
        super(NotWritableException, self).__init__(msg)


class NotReadableException(Exception):
    def __init__(self, attribute_name):
        msg = u"Attribute {} is not readable.".format(attribute_name)
        super(NotReadableException, self).__init__(msg)


def get_config_from_py_file(config_path):
    """
    Load a configuration from a .py file.

    @param config_path: Path to configuration file.
    @type config_path: str or unicode
    @return: Config as dict.
    @rtype: dict
    """
    config = types.ModuleType('config')
    config.__file__ = config_path
    try:
        with open(config_path) as config_file:
            exec(compile(config_file.read(), config_path, 'exec'),
                 config.__dict__)
    except IOError:
        pass  # Test will fail anyway
    return {
        key: getattr(config, key) for key in dir(config) if key.isupper()
    }


class ProtocolParsingException(Exception):

    def __init__(self, message):
        super(ProtocolParsingException, self).__init__(message)


class RuleApplicationException(Exception):

    def __init__(self, rule_name, rule_input):
        super(RuleApplicationException, self).__init__(
            u"Rule {} couldn't be applied to the following input {}.".format(
                rule_name, rule_input
            )
        )


class ParsingException(Exception):

    def __init__(self, message):
        super(ParsingException, self).__init__(message)