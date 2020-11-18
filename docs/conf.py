"""
=============================
Configuration file for Sphinx
=============================

Path Setup
==========
"""
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

import generic_lexer


"""
Project Information
===================
"""
project = generic_lexer.__package__
author = generic_lexer.__author__
maintainer = generic_lexer.__maintainer__
version = generic_lexer.__version__


"""
General Configuration
=====================
"""
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx_autodoc_typehints",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
html_theme = "nature"
