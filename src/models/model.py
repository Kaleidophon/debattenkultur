# -*- coding: utf-8 -*-

"""
Model superclass.
"""

# STD
import abc

# EXT
import cerberus

# PROJECT
from misc.custom_exceptions import NotWritableException, NotReadableException


class Model:
    """
    Model superclass.
    """
    __metaclass__ = abc.ABCMeta
    formatting_functions = {}
    internals = {
        "formatting_functions", "internals", "not_writable", "not_readable"
    }
    not_writable = set()
    not_readable = set()

    def __init__(self, formatting_functions={}, internals=set(),
                 not_writable=set(), not_readable=set(), **init_attributes):
        self.formatting_functions.update(formatting_functions)
        self.internals = self.internals.union(internals)

        for attribute, value in init_attributes.items():
            setattr(self, attribute, value)

        self.not_writable = self.not_writable.union(not_writable)
        self.not_readable = self.not_readable.union(not_readable)

    @property
    def attributes(self):
        return {
            key: value for key, value in self.__dict__.iteritems()
            if key not in self.internals
            and key not in self.not_readable
            and not key.startswith("_")
        }

    def __setattr__(self, key, value):
        if key in self.not_writable:
            raise NotWritableException(key)

        if key in self.formatting_functions:
            value = self.formatting_functions[key](value)

        super(Model, self).__setattr__(key, value)

    def __getattr__(self, item):
        if item in self.not_readable:
            raise NotReadableException(item)
        return super(Model, self).__getattribute__(item)

    def __str__(self):
        return "<{} #{}>".format(
            self.__class__.__name__,
            id(self)
        )


class Empty(Model):
    """
    Empty to model so in case parsing fails, not 'None's will be returned.
    """
    def __init__(self, exception=None):
        init_args = {}
        if exception:
            init_args["exception"] = exception.message
        super().__init__(**init_args)


class Filler(Model):
    """
    Model for filler lines that didn't trigger any parsing rules.
    """
    def __init__(self, line):
        super().__init__({"line": line})


class Target(Model):
    """
    Super class for target models that processed data from parser rules or
    parsers gets put into.
    """
    target_type = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.internals = self.internals.union(
            {"schema", "validator", "target_type"}
        )
        self.validate()

    def validate(self):
        """
        Validate the data in this target.
        """
        if self.schema == {}:
            raise AssertionError(
                "No validation schema was declared for this class."
            )

        if not self.validator.validate(self.attributes, self.schema):
            raise cerberus.DocumentError(
                "The following error were encountered during the validation "
                "of this {} target: {}".format(
                    self.target_type,
                    "\t* ".join(
                        [
                            "{}:{}".format(field, " / ".join(errors))
                            for field, errors in self.validator.errors()
                        ]
                    )
                )
            )

    @abc.abstractmethod
    @property
    def schema(self):
        """
        Define a data validation schema for the current class here.
        """
        return {}

    @property
    def validator(self):
        """
        Initialize the validator to validate data for this target.
        """
        return cerberus.Validator()


class RuleTarget(Target):
    """
    Super class for rule targets, to which all the lines a rule spans are
    combined to.
    """
    target_type = "rule"

    @abc.abstractmethod
    @property
    def schema(self):
        return {}


class ParserTargetValidator(cerberus.Validator):
    """
    Overriding the default cerberus validator to explicitly validate rule
    target models.
    """
    def _validate_type_ruletarget(self, value):
        """
        Implement extra function to validate RuleTargets.
        """
        return isinstance(value, RuleTarget)

    def _validate_type_parsertarget(self, value):
        """
        Implement extra function to validate ParserTargets (used in meta
        parser).
        """
        return isinstance(value, ParserTarget)


class ParserTarget(Target):
    """
    Super class for target models for parser, to which all the rule targets
    are combined to.
    """
    target_type = "parser"

    @abc.abstractmethod
    @property
    def schema(self):
        return {}

    @property
    def validate(self):
        """
        Initialize a special validator for parser targets.
        """
        return ParserTargetValidator()

