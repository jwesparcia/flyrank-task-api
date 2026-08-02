from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    
class TaskUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    done: Optional[bool] = None