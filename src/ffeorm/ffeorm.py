from typing import Callable

from ffeorm.databases import SqliteDb
from ffeorm.types import Entity, EntityConfiguration
from ffeorm.utils import SingletonMeta, SqliteQueriesBuilder
from ffeorm.utils.entity_parser import parse_entity


class Ffeorm(metaclass=SingletonMeta):
    def __init__(self, db_connection_string: str) -> None:
        self._entities: dict[str, Entity] = {}
        self._sqlite_db = SqliteDb(db_connection_string)

        self._sqlite_queries_builder = SqliteQueriesBuilder()

    @property
    def entities(self):
        return self._entities

    def entity(self, entity_configuration: EntityConfiguration) -> Callable:
        def decorator(entity: type):
            self._register_entity(parse_entity(entity, entity_configuration))

            return entity

        return decorator

    def _register_entity(self, entity: Entity) -> None:
        if entity["name"] in self._entities:
            raise ValueError(
                f"Entity with name {entity['name']} is already registered."
            )

        self._entities[entity["name"]] = entity
