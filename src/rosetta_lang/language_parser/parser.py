from . import rosetta_file
from .. import base_types


class Parser:
    parsed_lines = []

    def __init__(self, entrance: str):
        with rosetta_file.RosettaFile(entrance) as to_parse:
            for curr_line in to_parse:
                for regex, curr_class in base_types.RosettaBase.regex_iter():
                    if regex.match(curr_line):
                        print(curr_line)
