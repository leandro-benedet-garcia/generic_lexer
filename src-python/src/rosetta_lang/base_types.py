import enum
import typing


package_name = "Rosetta"


class RosettaBase:
    name: str
    owner_body: typing.List["RosettaBody"]


registered_bases: typing.Dict[str, RosettaBase] = {}


def register_base(
    entrance_class: typing.Type[RosettaBase], code_representation: string
) -> typing.Type[RosettaBase]:
    class_name = entrance_class.__name__
    class_mro = entrance_class.__mro__

    if RosettaBase not in class_mro:
        raise TypeError(
            "Class must inherit from RosettaBody or class inherited by it the class "
            f"{class_name} mro is {class_mro}"
        )

    class_name = class_name.replace(package_name, "")
    class_name = class_name.lower()

    registered_bases[class_name] = entrance_class

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
