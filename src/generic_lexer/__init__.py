# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
=============
Generic Lexer
=============
.. image:: {__badge_url}/badge/license-Unlicense-blue.svg
    :target: http://unlicense.org/
    :alt: License: Unlicense

.. image:: {__badge_url}/badge/code%20style-black-000000.svg
    :target: {__github_url}/psf/black
    :alt: Code style: Black

.. image:: {__badge_url}/github/workflow/status/cerberus1746/generic_lexer/Tox%20Testing%20Suite
    :target: {__github_url}/Cerberus1746/generic_lexer/actions?query=workflow%3A%22Tox+Testing+Suite%22
    :alt: GitHub Workflow Status

.. image:: {__badge_url}/codeclimate/coverage/Cerberus1746/generic_lexer
    :target: https://codeclimate.com/github/Cerberus1746/generic_lexer/code
    :alt: Code Climate Coverage

.. image:: {__badge_url}/codeclimate/coverage-letter/Cerberus1746/generic_lexer
    :target: https://codeclimate.com/github/Cerberus1746/generic_lexer
    :alt: Code Climate Graduation


{__description__}

The minimun python version is 3.6.1

:Version: {__version__}
:Maintainer: {__maintainer__}
:Author: {__author__}
:License: {__license__}


:Example:

If we try to execute the following code:

.. testcode:: module_sample

    from generic_lexer import Lexer

    rules = {{
        "VARIABLE": r"(?P<var_name>[a-z_]+): (?P<var_type>[A-Z]\\w+)",
        "EQUALS": r"=",
        "SPACE": r" ",
        "STRING": r"\\".*\\"",
    }}

    data = "first_word: String = \\"Hello\\""

    for curr_token in Lexer(rules, False, data):
        print(curr_token)

Will give us the following output:

.. testoutput:: module_sample

    VARIABLE({{'var_name': 'first_word', 'var_type': 'String'}}) at 0
    SPACE(' ') at 18
    EQUALS('=') at 19
    SPACE(' ') at 20
    STRING('"Hello"') at 21
"""
import re
import sys


__version__ = "1.1.2"
__license__ = "The Unlicense"
__author__ = "Eli Bendersky"
__author_email__ = "eliben@gmail.com"
__maintainer__ = "Leandro Benedet Garcia"
__maintainer_email__ = "cerberus1746@gmail.com"
__description__ = "A generic pattern-based Lexer/tokenizer tool."
__url__ = "https://github.com/Cerberus1746/generic_lexer/"
__min_python_version__ = (3, 6, 1)


if "sphinx" in sys.modules:  # pragma: no cover
    __badge_url = "https://img.shields.io"
    __github_url = "https://github.com"
    __doc__ = __doc__.format(**globals())


# +------------------------+
# | Version specific stuff |
# +------------------------+
if sys.version_info < __min_python_version__:  # pragma: no cover
    sys.exit(
        f"The package does not support the current python version ({sys.version}) "
        f"you must use Python {__min_python_version__} or above"
    )

# Python versions under 3.7 doesn't have Pattern or Match, so we use str instead as a type
# Python version 3.9 implements support for [] in Pattern and Match
# but this does not work with other versions
# (Long live Tox/Nox)
elif sys.version_info < (3, 7):
    PatternType = str
    MatchPattern = str
elif sys.version_info < (3, 9):
    PatternType = re.Pattern
    MatchPattern = re.Match
else:
    PatternType = re.Pattern[str]
    MatchPattern = re.Match[str]

from .lexer import Lexer
from .token import Token
from .errors import LexerError
from .logging import logger


__all__ = ["Lexer", "Token", "LexerError", "logger"]
