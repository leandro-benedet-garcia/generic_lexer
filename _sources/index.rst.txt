.. generic-lexer documentation master file, created by
   sphinx-quickstart on Sat Nov 14 18:38:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. automodule:: generic_lexer
   :members:


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Changelog
=========
1.1.1
------
Added
^^^^^^
- :class:`~generic_lexer.Token` can have multiple values,
  they can be set or get like the example in the :class:`~generic_lexer.Token` class.
- :class:`~generic_lexer.Lexer` can have patterns with named groups that
  can be acessed trough :class:`~generic_lexer.Token`.
