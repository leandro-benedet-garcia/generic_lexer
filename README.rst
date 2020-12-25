=============
generic_lexer
=============

.. image:: https://img.shields.io/badge/license-Unlicense-blue.svg
   :target: http://unlicense.org/
   :alt: License: Unlicense

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://img.shields.io/github/workflow/status/cerberus1746/generic_lexer/Tox%20Testing%20Suite
   :target: https://github.com/Cerberus1746/generic_lexer/actions?query=workflow%3A%22Tox+Testing+Suite%22
   :alt: GitHub Workflow Status

.. image:: https://img.shields.io/codeclimate/coverage/Cerberus1746/generic_lexer
   :target: https://codeclimate.com/github/Cerberus1746/generic_lexer/code
   :alt: Code Climate Coverage

.. image:: https://img.shields.io/codeclimate/coverage-letter/Cerberus1746/generic_lexer
   :target: https://codeclimate.com/github/Cerberus1746/generic_lexer
   :alt: Code Climate Graduation

The minimun python version is 3.6.1

:Original Author:
   Eli Bendersky <eliben@gmail.com> with
   `this gist <https://gist.github.com/eliben/5797351/>`_
   last modified on 2010/08
:Author:
   Leandro Benedet Garcia <cerberus1746@gmail.com>
:Version:
   1.1.2
:License:
   The Unlicense
:Documentation:
   The documentation can be found here:
   https://cerberus1746.github.io/generic_lexer/

Example
=======

If we try to execute the following code:

.. testcode:: module_sample

   from generic_lexer import Lexer

   rules = {
      "VARIABLE": r"(?P<var_name>[a-z_]+):(?P<var_type>[A-Z]\w+)",
      "EQUALS": r"=",
      "SPACE": r" ",
      "STRING": r"\".*\"",
   }

   data = "first_word:String = \"Hello\""

   for curr_token in Lexer(rules, skip_whitespace=False, text_buffer=data):
      print(curr_token)

Will give us the following output:

.. testoutput:: module_sample

   VARIABLE({'var_name': 'first_word', 'var_type': 'String'}) at 0
   SPACE(' ') at 17
   EQUALS('=') at 18
   SPACE(' ') at 19
   STRING('"Hello"') at 20
