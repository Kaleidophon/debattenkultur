# -*- coding: utf-8 -*-

"""
Helper functions and classes.
"""

# STD
import types


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
