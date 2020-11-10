from rosetta_lang import base_types
import sys
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_simple():
    """
    just to find a test
    """
    assert "namespace" in base_types.RosettaBase.base_names
