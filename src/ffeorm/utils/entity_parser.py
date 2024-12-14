import re
from types import GenericAlias
from typing import ForwardRef

from ffeorm.types import ComplexType, Entity, EntityConfiguration
from ffeorm.types.database_description import (
    ALLOWED_NESTED_TYPES,
    ALLOWED_PRIMITIVE_TYPES,
    BaseType,
    PrimitiveType,
)


def parse_entity(entity: type, config: EntityConfiguration) -> Entity:
    _check_entity_validity(entity, config)

    return {
        "name": entity.__name__,
        "columns": [
            {
                "name": column_name,
                "type": _get_type(column_type),
            }
            for column_name, column_type in entity.__annotations__.items()
        ],
        "configuration": config,
    }


def _get_type(column_type: type) -> PrimitiveType | ComplexType:
    if isinstance(column_type, ForwardRef):
        return {
            "base_type": BaseType.REFERENCE,
            "nested_entity": column_type.__forward_arg__,
        }

    if isinstance(column_type, GenericAlias):
        if column_type.__name__ not in ALLOWED_NESTED_TYPES:
            raise TypeError("Only list is allowed as a nested type.")

        base_type, nested_entity = _from_list_type(str(column_type))
        return {
            "base_type": base_type,
            "nested_entity": nested_entity,
        }

    if column_type.__name__ in ALLOWED_PRIMITIVE_TYPES:
        return column_type.__name__

    # TODO: Handle complex types
    return {
        "base_type": BaseType.REFERENCE,
        "nested_entity": column_type.__name__,
    }


def _from_list_type(type: str) -> tuple[BaseType, str]:
    match = re.search(r"__main__\.(\w+)", type)

    assert match, f"Could not extract nested entity from {type}."
    return BaseType.LIST, match.group(1)


def _check_entity_validity(entity: type, settings: EntityConfiguration) -> None:
    if not issubclass(entity, dict):
        raise TypeError("Entity must be a subclass of TypedDict.")

    attributes = entity.__annotations__

    if not attributes:
        raise ValueError("Entity must have at least one attribute.")

    if settings["auto_increment"] and "id" in attributes:
        raise ValueError(
            "Entity with auto-incrementing primary key cannot have an 'id' attribute."
        )

    if not settings["auto_increment"] and "id" not in attributes:
        raise ValueError(
            "Entity without auto-incrementing primary key must have an 'id' attribute."
        )
