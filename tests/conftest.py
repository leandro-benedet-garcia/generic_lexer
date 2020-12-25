import logging
import os
import pathlib
import pprint

import pytest


current_folder = pathlib.Path(__file__).parent


@pytest.fixture(scope="session")
def curr_logger() -> None:
    work_dir = pathlib.Path(os.getenv("TOX_WORK_DIR", current_folder))
    current_tox_env = os.getenv("TOX_ENV_NAME", "")
    file_logger = logging.FileHandler(
        work_dir / current_tox_env / "testing.log.rst", "w"
    )

    curr_logger = logging.getLogger()
    curr_logger.setLevel(logging.DEBUG)
    curr_logger.addHandler(file_logger)

    test_title = "PyTest"
    test_title_separator = "=" * len(test_title)

    curr_logger.debug(test_title_separator)
    curr_logger.debug(test_title)
    curr_logger.debug(test_title_separator + "\n")

    return curr_logger


@pytest.fixture(scope="session")
def text_to_parse() -> None:
    with open(current_folder / "text_to_parse.txt") as orig_text:
        return orig_text.read()


@pytest.fixture(scope="session")
def complex_token_dict() -> None:
    return {"first_var": "10", "second_var": "TESTING"}


@pytest.fixture(scope="session")
def tuple_rules() -> None:
    return (
        ("VARIABLE", r"(?P<var_name>[a-z_]+):(?P<var_type>[A-Z]\w+)"),
        ("NAMESPACE", r"namespace:(?P<namespace>[a-z]+)"),
        ("LB", r"\n"),
        ("EQUALS", r"="),
        ("SPACE", r" "),
        ("TAB", r"\t"),
        ("STRING", r"\"(?P<curr_str>.*)\""),
    )


@pytest.fixture(scope="session")
def dict_rules(tuple_rules) -> None:
    return dict(tuple_rules)


@pytest.fixture(scope="session")
def debug_log_code(curr_logger) -> None:
    def inner_debug_log_code(text_to_parse):
        pp = pprint.PrettyPrinter(width=100)

        out_str = pp.pformat(text_to_parse)
        out_str = out_str.replace("\n", "\n    ")
        curr_logger.debug("\n.. code :: python\n\n    " + out_str)

    return inner_debug_log_code
