from collections import namedtuple
from typing import Optional, Iterator

from .SQLite import Sqlite3_Database


class Task:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.user_id: int = kwargs.get('user_id')
            self.title: str = kwargs.get('title')
            self.description: str = kwargs.get('description')
        else:
            self.user_id: Optional[int] = None
            self.title: Optional[str] = None
            self.description: Optional[str] = None

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Tasks(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.new_id = len(self.get_keys())

    def add(self, obj: Task) -> None:
        self.add_row(obj)
        self.new_id += 1

    def __delitem__(self, key):
        self.del_instance(key)

    def __iter__(self) -> Iterator[Task]:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user

    def get_tasks_user(self, user_id: int) -> list[Task] | None:
        data = self.get_by_other_field(value=user_id, field="user_id", args="*")
        if len(data) == 0:
            return None
        tasks = []
        for data_task in data:
            tasks.append(Task(id=data_task[0],
                              user_id=data_task[1],
                              title=data_task[2],
                              description=data_task[3],
                              ))

        return tasks

    def get(self, id: int) -> Task | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Task(id=obj_tuple[0],
                       user_id=obj_tuple[1],
                       title=obj_tuple[2],
                       description=obj_tuple[3])
            return obj
        return False
