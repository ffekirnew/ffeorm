from typing import TypedDict

from ffeorm.ffeorm import Ffeorm

orm = Ffeorm("university")


@orm.entity({"auto_increment": True})
class Course(TypedDict):
    department: "Department"
    title: str
    credits: int


@orm.entity({"auto_increment": True})
class Professor(TypedDict):
    name: str
    age: int
    department: "Department"


@orm.entity({"auto_increment": True})
class Department(TypedDict):
    name: str
    location: str
    professors: list[Professor]
    courses: list[Course]


@orm.entity({"auto_increment": True})
class Student(TypedDict):
    name: str
    age: int
    department: Department
    courses: list[Course]


@orm.entity({"auto_increment": True})
class School(TypedDict):
    name: str
    location: str
    departments: list[Department]
    students: list[Student]


__import__("pprint").pprint(orm.entities)
