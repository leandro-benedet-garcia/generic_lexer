import re
import typing
from typing import Dict, Iterator, Mapping, Set

from . import MatchPattern, token
from .errors import LexerError


class Lexer:
    """
    A simple pattern-based lexer/tokenizer.
    All the regexes are concatenated into a single one with named groups.
    The group names must be valid Python identifiers.
    The patterns without groups auto generate them.
    Groups are then mapped to token names.

    :param rules: A list of rules. Each rule is a :class:`str` pair,
        where the first is the type of the token
        to return when it's recognized and the second
        is the regular expression used to recognize the token.
    :param skip_whitespace: If True, whitespace (\\s+) will be skipped and not
        reported by the lexer. Otherwise, you have to specify your rules for
        whitespace, or it will be flagged as an error.
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
        rules: Mapping[str, str],
        skip_whitespace: bool = False,
        text_buffer: str = "",
    ):
        # set parameters into attributes
        self._skip_whitespace = skip_whitespace
        self.text_buffer = text_buffer

        # inicialize variables that will be used
        self._pattern_id = 0
        self._re_ws_skip = re.compile(r"\S")
        self._regex_parts: Set[str] = set()
        self._group_type: Dict[str, str] = {}

        for token_name, pattern in rules.items():
            self.pattern_token(token_name, pattern)

        self._lexer_pattern = re.compile("|".join(self._regex_parts))

    def __iter__(self) -> Iterator[token.Token]:
        yield from self.tokens()

    @property
    def current_char(self) -> str:
        return self.get_char_at_current_pointer()

    # Text buffer property
    def get_text_buffer(self) -> str:
        """
        Get the current text to be parsed into the lexer
        """
        return self._text_buffer

    def set_text_buffer(self, value: str) -> None:
        """
        Set the text to be parsed into the lexer and set the pointer back to 0
        """
        self._text_buffer_pointer = 0
        self._text_buffer = value

    def clear_text_buffer(self) -> None:
        """
        Set the text buffer to a blank string and set the text pointer to 0
        """
        self._text_buffer_pointer = 0
        self._text_buffer = ""

    text_buffer: str = typing.cast(
        str,
        property(
            get_text_buffer,
            set_text_buffer,
            clear_text_buffer,
            "Set, Get or Clear the text buffer, you may use :keyword:`del` "
            "with this property to clear the text buffer",
        )
    )

    def get_char_at_current_pointer(self) -> str:
        return self.get_char_at(self._text_buffer_pointer)

    def get_char_at(self, buffer_pointer: int) -> str:
        return self.text_buffer[buffer_pointer]

    def pattern_token(self, token_name: str, pattern: str) -> None:
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

    def tokens(self, skip_whitespace: bool = False) -> Iterator[token.Token]:
        """
        :param skip_whitespace: just like :attr:`Lexer.skip_whitespace`
            passed trough :class:`lexer.Lexer` for the current method call.
        :raises generic_lexer.errors.LexerError: raised with the position and
            character of the error in case of a lexing error
            (if the current chunk of the buffer matches no rule).
        :yields: the next token (a Token object) found in the
            :attr:`Lexer.text_buffer`.
        """
        while self._text_buffer_pointer < len(self.text_buffer):
            if skip_whitespace or self._skip_whitespace:
                regex_match = self._re_ws_skip.search(
                    self.text_buffer, self._text_buffer_pointer
                )

                if regex_match:
                    self._text_buffer_pointer = regex_match.start()
                else:
                    break

            regex_match = self._lexer_pattern.match(
                self.text_buffer, self._text_buffer_pointer
            )

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

    def _generate_token_from_match(
        self, regex_match: MatchPattern
    ) -> token.Token:
        token_vars = {}
        all_groups = regex_match.groupdict().items()

        for curr_group, curr_value in all_groups:
            if curr_value:
                token_vars[curr_group] = curr_value

        token_name = self._group_type[str(regex_match.lastgroup)]

        created_token = token.Token(
            token_name, self._text_buffer_pointer, token_vars
        )
        self._text_buffer_pointer = regex_match.end()

        return created_token


__all__ = ["Lexer"]
