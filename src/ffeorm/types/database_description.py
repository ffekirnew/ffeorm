from enum import StrEnum
from typing import Annotated, NotRequired, TypedDict

from ffeorm.types.entity_settings import EntityConfiguration

PrimitiveType = Annotated[str, "Built-in types"]
ALLOWED_PRIMITIVE_TYPES = set(["str", "int", "float", "bool"])
ALLOWED_NESTED_TYPES = set(["list"])


class BaseType(StrEnum):
    NONE = "None"
    LIST = "list"
    DICT = "dict"
    REFERENCE = "reference"


class ComplexType(TypedDict):
    base_type: BaseType
    nested_entity: str


class ForeignKey(TypedDict):
    table: str
    column: str


class Column(TypedDict):
    name: str
    type: PrimitiveType | ComplexType
    primary_key: NotRequired[bool]
    nullable: NotRequired[bool]
    foreign_key: NotRequired[ForeignKey]
    unique: NotRequired[bool]


class Entity(TypedDict):
    name: str
    columns: list[Column]
    configuration: EntityConfiguration
