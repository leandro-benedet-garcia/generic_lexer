# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
=============
Generic Lexer
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


{__description__}

The minimun python version is 3.6

:Version: {__version__}
:Maintainer: {__maintainer__}
:Author: {__author__}
:License: {__license__}

:Example:

If we try to execute the following code:

.. testcode:: module_sample

    from generic_lexer import Lexer

    rules = {{
        "VARIABLE": r"(?P<var_name>[a-z_]+): (?P<var_type>[A-Z]\w+)",
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
    SPACE( ) at 18
    EQUALS(=) at 19
    SPACE( ) at 20
    STRING("Hello") at 21
"""
import re
import sys
from typing import Dict, ItemsView, Iterable, Iterator, List, Set, Tuple, Union


__version__ = "1.1.1"
__license__ = "The Unlicense"
__author__ = "Eli Bendersky"
__author_email__ = "eliben@gmail.com"
__maintainer__ = "Leandro Benedet Garcia"
__maintainer_email__ = "cerberus1746@gmail.com"
__description__ = "A generic pattern-based Lexer/tokenizer tool."
__url__ = "https://github.com/Cerberus1746/generic_lexer/"
__min_python_version__ = (3, 6)


if "sphinx" in sys.modules:  # pragma: no cover
    __doc__ = __doc__.format(**globals())

if sys.version_info < __min_python_version__:  # pragma: no cover
    sys.exit(
        f"The package does not support the current python version ({sys.version}) "
        f"you must use Python {__min_python_version__} or above"
    )
elif sys.version_info < (3, 7):
    # Python versions under 3.7 doesn't have Pattern or Match, so we use str instead as a type
    PatternType = str
    MatchPattern = str
else:
    PatternType = re.Pattern
    MatchPattern = re.Match


class Token:
    """
    A simple Token structure. Contains the token name, value and position.

    As you can see differently from the original gist,
    we are capable of specifying multiple groups per token.

    You may get the values of the tokens this way:

    .. doctest:: token_sample

        >>> from generic_lexer import Lexer
        >>> rules = {
        ...     "VARIABLE": r"(?P<var_name>[a-z_]+): (?P<var_type>[A-Z]\w+)",
        ...     "EQUALS": r"=",
        ...     "STRING": r"\\".*\\"",
        ... }
        >>> data = "first_word: String = \\"Hello\\""
        >>> variable, equals, string = tuple(Lexer(rules, True, data))

        >>> variable
        VARIABLE({'var_name': 'first_word', 'var_type': 'String'}) at 0

        >>> variable.val
        {'var_name': 'first_word', 'var_type': 'String'}
        >>> variable["var_name"]
        'first_word'
        >>> variable["var_type"]
        'String'

        >>> equals
        EQUALS(=) at 19

        >>> equals.val
        '='

        >>> string
        STRING("Hello") at 21

        >>> string.val
        '"Hello"'

    :param name: the name of the token
    :param position: the position the token was found in the text buffer
    :param val: token's value
    """

    __slots__ = ("_val", "name", "position")

    def __init__(self, name, position, val):
        self.name: str = name
        self._val: Dict[str, str] = val
        self.position: int = position

    @property
    def val(self) -> Union[Dict[str, str], str]:
        if len(self._val) == 1:
            return next(iter(self._val.values()))

        return self._val

    def __repr__(self):
        values = str(self.val).replace("\n", "\\n")
        values = values.replace("\t", "\\t")

        return f"{self.name}({values}) at {self.position}"

    def __getitem__(self, key):
        return self._val[key]

    __str__ = __repr__


class LexerError(Exception):
    """
    Lexer error exception.

    :param text_buffer_pointer: position in the input_buf line where the error occurred.
    :param char: the character that triggered the error
    """

    __slots__ = ("text_buffer_pointer", "char")

    def __init__(self, char: str, text_buffer_pointer: int):
        self.text_buffer_pointer = text_buffer_pointer
        self.char = char

    def __repr__(self):
        return f'The char "{self.char}" at position {self.text_buffer_pointer} is not a valid Token'

    __str__ = __repr__


class Lexer:
    """
    A simple pattern-based lexer/tokenizer.

    All the regexes are concatenated into a single one with named groups. The group names
    must be valid Python identifiers. The patterns without groups auto generate them.
    Groups are then mapped to token names.

    :param rules: A list of rules. Each rule is a :class:`str`, :class:`re.Pattern` pair, where
        :class:`str` is the type of the token to return when it's recognized and
        :class:`re.Pattern` is the regular expression used to recognize the token.
    :param skip_whitespace: If True, whitespace (\s+) will be skipped and not reported by the
        lexer. Otherwise, you have to specify your rules for whitespace, or it will be flagged
        as an error.
    :param text_buffer: the string to generate the tokens from
    """

    __slots__ = (
        "_pattern_id",
        "_regex_parts",
        "_skip_whitespace",
        "_text_buffer",
        "_re_ws_skip",
        "_group_type",
        "_text_buffer_pointer",
        "_lexer_pattern",
        "_finished_token_generation",
        "_token_list",
    )

    def __init__(
        self,
        rules: Union[Dict[str, PatternType], Iterable[Tuple[str, PatternType]]],
        skip_whitespace: bool = False,
        text_buffer: str = "",
    ):
        # set parameters into attributes
        self._skip_whitespace: bool = skip_whitespace
        self.text_buffer = text_buffer

        # inicialize variables that will be used
        self._pattern_id: int = 0
        self._re_ws_skip: PatternType = re.compile("\S")
        self._regex_parts: Set[str] = set()
        self._token_list: List[Token] = []
        self._group_type: Dict[str, str] = {}

        if isinstance(rules, dict):
            rules = rules.items()

        for token_name, pattern in rules:
            self.pattern_token(token_name, pattern)

        self._lexer_pattern = re.compile("|".join(self._regex_parts))

    def __iter__(self):
        yield from self.tokens()

    @property
    def current_char(self):
        return self.get_char_at_current_pointer()

    # Text buffer property
    def get_text_buffer(self) -> str:
        """
        Get the current text to be parsed into the lexer
        """
        return self._text_buffer

    def set_text_buffer(self, value: str):
        """
        Set the text to be parsed into the lexer and set the pointer back to 0
        """
        self._text_buffer_pointer = 0
        self._text_buffer = value

    def clear_text_buffer(self):
        """
        Set the text buffer to a blank string and set the text pointer to 0
        """
        self._text_buffer_pointer = 0
        self._text_buffer = ""

    text_buffer = property(
        get_text_buffer,
        set_text_buffer,
        clear_text_buffer,
        "Set, Get or Clear the text buffer, you may use :keyword:`del` "
        "with this property to clear the text buffer",
    )

    def get_char_at_current_pointer(self) -> str:
        return self.get_char_at(self._text_buffer_pointer)

    def get_char_at(self, buffer_pointer: int) -> str:
        return self.text_buffer[buffer_pointer]

    def pattern_token(self, token_name, pattern):
        group_keys = re.compile(pattern).groupindex.keys()

        if any(group_keys):
            for curr_group in group_keys:
                self._regex_parts.add(pattern)
                self._group_type[curr_group] = token_name

        else:
            groupname = f"GROUP{self._pattern_id}"
            self._group_type[groupname] = token_name

            self._regex_parts.add(f"(?P<{groupname}>{pattern})")
            self._pattern_id += 1

    def tokens(self, skip_whitespace: bool = False) -> Iterator[Token]:
        """
        :param skip_whitespace: just like :attr:`Lexer.skip_whitespace` passed trough
            :class:`Lexer` for the current method call.
        :raises LexerError: raised with the position and character of the error in case
            of a lexing error (if the current chunk of the buffer matches no rule).
        :yields: the next token (a Token object) found in the :attr:`Lexer.text_buffer`.
        """
        while self._text_buffer_pointer < len(self.text_buffer):
            if skip_whitespace or self._skip_whitespace:
                regex_match = self._re_ws_skip.search(self.text_buffer, self._text_buffer_pointer)

                if regex_match:
                    self._text_buffer_pointer = regex_match.start()
                else:
                    break

            regex_match = self._lexer_pattern.match(self.text_buffer, self._text_buffer_pointer)

            if regex_match:
                yield self._generate_token_from_match(regex_match)
            else:
                # if we're here, no rule matched
                raise LexerError(
                    text_buffer_pointer=self._text_buffer_pointer,
                    char=self.current_char,
                )

        self._text_buffer_pointer = 0
        self._finished_token_generation = True

    def _generate_token_from_match(self, regex_match: MatchPattern) -> Token:
        token_vars = {}
        all_groups: ItemsView[str, str] = regex_match.groupdict().items()

        for curr_group, curr_value in all_groups:
            if curr_value:
                token_vars[curr_group] = curr_value

        token_name = self._group_type[str(regex_match.lastgroup)]

        created_token = Token(token_name, self._text_buffer_pointer, token_vars)
        self._text_buffer_pointer = regex_match.end()

        return created_token
