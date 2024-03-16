from .start import start_rt
from .create_task import creat_rt
from .view_task import view_task_rt
from .del_task import del_task_rt
from .change_task import change_task_rt

routers = (start_rt, creat_rt, view_task_rt, del_task_rt, change_task_rt)
