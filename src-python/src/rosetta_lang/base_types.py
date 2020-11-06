import enum
import typing
import re


language_name = "Rosetta"


class RosettaBase:
    name: str
    owner_body: typing.List[language_name + "Body"]


class Bases:
    def __init__(self):
        self.registered_bases: typing.Set[RosettaBase] = set()
        self.base_names: typing.Set[str] = set()


    def register_base(
        self, entrance_class: typing.Type[RosettaBase], code_representation: str
    ) -> typing.Type[RosettaBase]:
        class_name = entrance_class.__name__
        class_mro = entrance_class.__mro__

        if RosettaBase not in class_mro:
            raise TypeError(
                f"Class must inherit from {language_name}Base {class_name} mro is {class_mro}"
            )

        class_name = class_name.replace(language_name, "")
        class_name = class_name.lower()

        self.registered_bases.append(entrance_class)

        return entrance_class


class Access(enum.Enum):
    PRIVATE: int
    PROTECTED: int
    PUBLIC: int


class RosettaBody(RosettaBase):
    body: typing.List[RosettaBase]


class RosettaAccess(RosettaBase):
    access: Access


@register_base
class RosettaVariable(RosettaAccess):
    rosetta_type: RosettaBase
    value: typing.Optional[RosettaBase]


@register_base
class RosettaFunction(RosettaBody, RosettaAccess):
    attributes: typing.List[RosettaVariable]


@register_base
class RosettaClass(RosettaBody):
    constructor: typing.Optional[RosettaFunction]
    child_declaration: typing.Optional[RosettaFunction]
    before_child_constructor: typing.Optional[RosettaFunction]


@register_base()
class RosettaNamespace(RosettaBody):
    pass
