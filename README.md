# Generic Lexer
[![image](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![image](https://img.shields.io/github/workflow/status/cerberus1746/generic_lexer/Tox%20Testing%20Suite)](https://github.com/Cerberus1746/generic_lexer/actions?query=workflow%3A%22Tox+Testing+Suite%22)
[![image](https://img.shields.io/codeclimate/coverage/Cerberus1746/generic_lexer)](https://codeclimate.com/github/Cerberus1746/generic_lexer/code)
[![image](https://img.shields.io/codeclimate/coverage-letter/Cerberus1746/generic_lexer)](https://codeclimate.com/github/Cerberus1746/generic_lexer)

A generic pattern-based Lexer/tokenizer tool.

The minimum python version is 3.6

<dl>
    <dt>Original Author</dt>
    <dd>
        <a href="mailto:eliben@gmail.com">Eli Bendersky</a> with
        <a href="https://gist.github.com/eliben/5797351">this gist</a> last modified on 2010/08</dd>
    <dt>Maintainer</dt>
    <dd>
        <a href="mailto:cerberus1746@gmail.com">Leandro Benedet Garcia</a> last modified on 2020/11
    </dd>
    <dt>Version</dt>
    <dd>1.1.1</dd>
    <dt>License</dt>
    <dd>The Unlicense</dd>
    <dt>Documentation</dt>
    <dd>
        The documentation can be <a href="https://cerberus1746.github.io/generic_lexer/">
            found here
        </a>
    </dd>
</dl>

## Example
If we try to execute the following code:

```python
from generic_lexer import Lexer


rules = {
    "VARIABLE": r"(?P<var_name>[a-z_]+): (?P<var_type>[A-Z]\w+)",
    "EQUALS": r"=",
    "SPACE": r" ",
    "STRING": r"\".*\"",
}

data = "first_word: String = \"Hello\""
data = data.strip()

for curr_token in Lexer(rules, False, data):
    print(curr_token)
```

Will give us the following output:

```python
VARIABLE({'var_name': 'first_word', 'var_type': 'String'}) at 0
SPACE( ) at 18
EQUALS(=) at 19
SPACE( ) at 20
STRING("Hello") at 21
```

As you can see differently from the original gist, we are capable of specifying multiple groups per token.
You cannot use the same group twice,
either per token or not because all the regex patterns are merged together to generate the tokens later on.

You may get the values of the tokens this way:

```python
>>> from generic_lexer import Lexer
>>> rules = {
...     "VARIABLE": r"(?P<var_name>[a-z_]+): (?P<var_type>[A-Z]\w+)",
...     "EQUALS": r"=",
...     "STRING": r"\".*\"",
... }
>>> data = "first_word: String = \"Hello\""
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
```
