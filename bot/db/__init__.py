from .Tasks import Task, Tasks

db_file_name = "bot/db/database"
tasks = Tasks(db_file_name=db_file_name, table_name="tasks")
__all__ = ("Task", "Tasks", "tasks")
