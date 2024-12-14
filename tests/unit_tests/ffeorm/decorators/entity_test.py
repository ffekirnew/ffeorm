from typing import TypedDict

from src.ffeorm.decorators.entity import entity


def test_entity():
    @entity(auto_increment=True, table_name="test_table")
    class TestEntity(TypedDict):
        pass
