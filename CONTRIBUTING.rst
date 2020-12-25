.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/Cerberus1746/generic_lexer/issues.

If you are reporting a bug, please include:

*  Your operating system name and version.
*  Any details about your local setup that might be helpful in troubleshooting.
*  Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

generic_lexer could always use more documentation, whether as part of the
official generic_lexer docs, in docstrings, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/Cerberus1746/generic_lexer/issues.

If you are proposing a feature:

*  Explain in detail how it would work.
*  Keep the scope as narrow as possible, to make it easier to implement.
*  Remember that this is a volunteer-driven project, and that contributions
   are welcome :)

Get Started!
------------

Ready to contribute?
Here's how to set up `generic_lexer` for local development.

#. Fork the `generic_lexer` repo on GitHub.
#. Clone your fork locally::

   $ git clone git@github.com:your_name_here/generic_lexer.git

#. Install pipenv following the instructions here:

   https://pipenv.pypa.io/en/latest/install/#installing-pipenv

#. Create a branch for local development::

   $ git checkout -b name-of-your-bugfix-or-feature

#. Create the virtual env and dev dependencies `--dev` is necessary because of
   `black`::

   $ pipenv install --dev --pre

   Now you can make your changes locally.

#. To run all tests you need to install tox with::

   $ pip install tox

   pipenv already installs all other dependencies automatically into your
   virtual enviroment

#. Commit your changes and push your branch to GitHub::

   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

#. The pull request should include tests.
#. It also should pass linting checks.
#. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
#. The pull request should work for Python 3.6, 3.7, 3.8 and
   3.9, and for PyPy3. Check
   https://github.com/Cerberus1746/generic_lexer/actions.

Tips
----

To run a subset of tests::

   $ pip install tox
   $ tox
