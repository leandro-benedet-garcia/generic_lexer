import re
import typing
import enum

language_name = "Rosetta"


class RosettaBase:
    name: str
    owner_body: typing.List[language_name + "Body"]

    registered_bases: typing.List[language_name + "Base"] = []
    base_names: typing.List[str] = []
    base_regexes: typing.List[re.Pattern] = []

    def __init_subclass__(cls, *args, code_regex=None, **kwargs):
        if code_regex:
            class_name = cls.__name__

            class_name = class_name.replace(language_name, "")
            class_name = class_name.lower()

            code_regex = code_regex.format(code_name=class_name)
            code_regex = re.compile(r"^" + code_regex, re.MULTILINE | re.DOTALL)

            RosettaBase.base_regexes.append(code_regex)
            RosettaBase.base_names.append(class_name)
            RosettaBase.registered_bases.append(cls)

        return super().__init_subclass__(*args, **kwargs)


class Access(enum.Enum):
    PRIVATE: int
    PROTECTED: int
    PUBLIC: int


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


class RosettaNamespace(RosettaBody, code_regex=r" *{code_name}:(?P<element_name>[a-z]+)"):
    pass
