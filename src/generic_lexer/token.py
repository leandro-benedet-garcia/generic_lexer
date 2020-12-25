from typing import Any, Dict, Union

from . import lexer


class Token:
    """
    A simple Token structure. Contains the token name, value and position.

    As you can see differently from the original gist,
    we are capable of specifying multiple groups per token.

    You may get the values of the tokens this way:

    .. doctest:: token_sample

        >>> from generic_lexer import Lexer
        >>> rules = {
        ...     "VARIABLE": r"(?P<var_name>[a-z_]+):(?P<var_type>[A-Z]\\w+)",
        ...     "EQUALS": r"=",
        ...     "STRING": r"\\".*\\"",
        ... }
        >>> data = "first_word:String = \\"Hello\\""
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
        EQUALS('=') at 18

        >>> equals.val
        '='

        >>> string
        STRING('"Hello"') at 20

        >>> string.val
        '"Hello"'

    :param name: the name of the token
    :param position: the position the token was found in the text buffer
    :param val: token's value
    """

    __slots__ = ("_val", "name", "position", "lexer")

    lexer: "lexer.Lexer"

    def __init__(self, name: str, position: int, val: Any):
        self.name: str = name
        self._val: Dict[str, str] = val
        self.position: int = position

    @property
    def val(self) -> Union[Dict[str, str], str]:
        if len(self._val) == 1:
            return next(iter(self._val.values()))

        return self._val

    @property
    def type(self) -> str:
        """
        For compability
        """
        return self.name

    def __repr__(self) -> str:
        return f"{self.name}({repr(self.val)}) at {self.position}"

    def __getitem__(self, key: str) -> str:
        return self._val[key]

    __str__ = __repr__


__all__ = ["Token"]
