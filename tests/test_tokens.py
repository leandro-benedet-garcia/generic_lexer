import generic_lexer

def test_generate_token():
    complex_dict = {
        "first_var": "10",
        "second_var": "TESTING"
    }

    complex_token = generic_lexer.Token("GROUP1", 0, complex_dict)

    assert complex_token.val == complex_dict
