import pytest

from generic_lexer import errors, lexer, token


def test_generate_token(complex_token_dict) -> None:
    simple_token = token.Token("GROUP1", 0, {"VAR": "Hello"})
    complex_token = token.Token("GROUP1", 0, complex_token_dict)

    assert complex_token.val == complex_token_dict
    assert simple_token.val == "Hello"


def test_lexer(debug_log_code, curr_logger, dict_rules, text_to_parse) -> None:
    tabbed_input = text_to_parse.replace("    ", "\t")

    parse_text_title = "Using this text to parse:"
    curr_logger.debug(parse_text_title)
    curr_logger.debug("=" * len(parse_text_title))

    lexer_with_whitespace = lexer.Lexer(dict_rules, text_buffer=tabbed_input)
    lexer_without_whitespace = lexer.Lexer(dict_rules, True, tabbed_input)

    repr_test = list(map(repr, lexer_with_whitespace))
    debug_log_code(repr_test)

    assert repr_test == [
        "NAMESPACE('paletter') at 0",
        "LB('\\n') at 18",
        "TAB('\\t') at 19",
        "VARIABLE({'var_name': 'name', 'var_type': 'String'}) at 20",
        "SPACE(' ') at 31",
        "EQUALS('=') at 32",
        "SPACE(' ') at 33",
        "STRING('test') at 34",
        "LB('\\n') at 40",
    ]

    assert list(map(repr, lexer_without_whitespace)) == [
        "NAMESPACE('paletter') at 0",
        "VARIABLE({'var_name': 'name', 'var_type': 'String'}) at 20",
        "EQUALS('=') at 32",
        "STRING('test') at 34",
    ]

    curr_lexer_list = list(lexer_with_whitespace)
    curr_lexer_without_whitespace_list = list(lexer_without_whitespace)

    assert any(curr_lexer_list)
    assert any(curr_lexer_without_whitespace_list)

    debug_log_code(curr_lexer_list)
    debug_log_code(curr_lexer_without_whitespace_list)

    del lexer_with_whitespace.text_buffer
    assert not any(lexer_with_whitespace.text_buffer)


def test_lexer_exception(dict_rules) -> None:
    with pytest.raises(errors.LexerError):
        try:
            tuple(lexer.Lexer(dict_rules, text_buffer="46545das"))
        except errors.LexerError as lexer_error:
            assert lexer_error.char == "4"
            assert lexer_error.text_buffer_pointer == 0

            raise lexer_error
