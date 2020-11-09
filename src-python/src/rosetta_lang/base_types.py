import re
import typing

from . import mini_enum


language_name = "Rosetta"


class RosettaBase:
    name: str
    owner_body: typing.List[language_name + "Body"]

    _registered_bases = []
    _base_names = []
    _base_regexes = []

    def __init_subclass__(cls, *args, **kwargs):
        if hasattr(cls, "code_regex"):
            # Creation of the dynamic init, like in dataclass
            cls.__annotations__ = {**RosettaBase.__annotations__, **cls.__annotations__}

            annotation_keys = cls.__annotations__.keys()
            local_vars = ", ".join(annotation_keys)

            txt = f"def __generated_init(self, {local_vars}):\n"
            txt += "\n".join(f"  self.{b} = {b}" for b in annotation_keys)
            txt += "\ncls.__init__ = __generated_init"

            exec(txt)

            # Add the class to the language bases
            class_name = cls.__name__

            class_name = class_name.replace(language_name, "")
            class_name = class_name.lower()

            code_regex = cls.code_regex.format(code_name=class_name)
            code_regex = re.compile(r"^" + code_regex, re.X)

            RosettaBase._base_regexes.append(code_regex)
            RosettaBase._base_names.append(class_name)
            RosettaBase._registered_bases.append(cls)

        return super().__init_subclass__(*args, **kwargs)

    @classmethod
    def regex_iter(cls) -> typing.Generator[typing.Tuple[re.Pattern, "RosettaBase"], None, None]:
        """
        :yields: a generator that returns a pair of a compiled regex and the class linked to it
        """
        for curr_re, curr_class in zip(cls._base_regexes, cls._registered_bases):
            yield curr_re, curr_class

    @classmethod
    def name_iter(cls):
        """
        :yields: a generator that returns a pair of a compiled regex and the class linked to it
        """
        for curr_name, curr_class in zip(cls._base_names, cls._registered_bases):
            yield curr_name, curr_class


Access = mini_enum.MiniEnum("PRIVATE", "PROTECTED", "PUBLIC")


class RosettaBody(RosettaBase):
    body: typing.List[RosettaBase]


class RosettaAccess(RosettaBase):
    access: Access


class RosettaVariable(RosettaAccess):
    rosetta_type: RosettaBase
    value: typing.Optional[RosettaBase]


class RosettaFunction(RosettaBody, RosettaAccess):
    attributes: typing.List[RosettaVariable]


class RosettaClass(RosettaBody):
    constructor: typing.Optional[RosettaFunction]
    child_declaration: typing.Optional[RosettaFunction]
    before_child_constructor: typing.Optional[RosettaFunction]


class RosettaNamespace(RosettaBody):
    code_regex: re.Pattern = r"{code_name}:(?P<element_name>[a-z]+)"


if __name__ == "__main__":
    print(RosettaBase._base_names)
