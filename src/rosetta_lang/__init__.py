"""
Main module for the programming language
"""
from . import __version__, base_types, mini_enum

language_version = __version__.__version__

__all__ = ["base_types", "mini_enum", "language_version"]
