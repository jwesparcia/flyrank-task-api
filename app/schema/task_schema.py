from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    id: int
    title: str
    
class TaskUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    done: Optional[bool] = None