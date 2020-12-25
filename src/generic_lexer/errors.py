class LexerError(Exception):
    """
    Lexer error exception.

    :param text_buffer_pointer: position in the input_buf line
        where the error occurred.
    :param char: the character that triggered the error
    """

    __slots__ = ("text_buffer_pointer", "char")

    def __init__(self, char: str, text_buffer_pointer: int):
        self.text_buffer_pointer = text_buffer_pointer
        self.char = char

    def __repr__(self) -> str:
        return (
            f"The char '{self.char}' at position "
            f"{self.text_buffer_pointer} is not a valid Token"
        )

    __str__ = __repr__


__all__ = ["LexerError"]
