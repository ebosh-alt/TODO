from typing import Optional

from pydantic import BaseModel


class ModelTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

