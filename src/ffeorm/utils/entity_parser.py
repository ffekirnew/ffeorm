import re
from types import GenericAlias
from typing import ForwardRef, TypedDict, _TypedDict

from ffeorm.types import ComplexType, Entity, EntityConfiguration
from ffeorm.types.database_description import (
    ALLOWED_NESTED_TYPES,
    ALLOWED_PRIMITIVE_TYPES,
    BaseType,
    PrimitiveType,
)


class EntityParser:
    def __init__(self) -> None:
        self._tables: dict[str, Entity] = {}

    def parse_entity(self, entity: type, config: EntityConfiguration) -> Entity:
        entity_name = entity.__name__
        if entity.__name__ in self._tables:
            raise ValueError(f"Entity {entity_name} already registered.")

        return {
            "name": entity_name,
            "columns": [
                {
                    "name": column_name,
                    "type": self._get_type(column_type),
                }
                for column_name, column_type in entity.__annotations__.items()
            ],
            "configuration": config,
        }

    def _get_type(self, column_type: type) -> PrimitiveType | ComplexType:
        if isinstance(column_type, ForwardRef):
            return {
                "base_type": BaseType.REFERENCE,
                "nested_entity": column_type.__forward_arg__,
            }

        if isinstance(column_type, GenericAlias):
            if column_type.__name__ not in ALLOWED_NESTED_TYPES:
                raise TypeError("Only list is allowed as a nested type.")

            base_type, nested_entity = self._from_list_type(str(column_type))
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

    def _from_list_type(self, type: str) -> tuple[BaseType, str]:
        match = re.search(r"__main__\.(\w+)", type)

        assert match, f"Could not extract nested entity from {type}."
        return BaseType.LIST, match.group(1)
