import os
import pathlib
import typing


class RosettaFile:
    """
    Class that holds data of the file code

    :param to_parse: is a :class:`os.PathLike` string or object that is the file to read from
    """
    def __init__(
        self,
        to_parse: typing.Union[str, bytes, os.PathLike],
        *args: typing.List[typing.Union[str, int]],
        **kwargs: typing.Mapping[str, typing.Union[str, int]]
    ):

        self._opened_file = pathlib.Path(to_parse).open(*args, **kwargs)

        read_file = self._opened_file.read()

        while "\n\n" in read_file:
            read_file = read_file.replace("\n\n", "\n")

        read_file = read_file.replace("    ", "\t")

        self._splitted = read_file.split("\n")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._opened_file.close()

    def __iter__(self):
        self._curr_iter = -1
        return self

    def __next__(self):
        self._curr_iter += 1
        if self._curr_iter < len(self._splitted):
            return self._splitted[self._curr_iter]

        raise StopIteration
