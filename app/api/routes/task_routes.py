from fastapi import APIRouter, HTTPException, Response
from app.schema.task_schema import TaskCreate
from app.schema.task_schema import TaskUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.task import Task
from dependencies.database import get_db
router = APIRouter(
    prefix = "/tasks",
    tags = ["Tasks"]
)

tasks = [
        {"id": 1, "title": "Go to gym.", "done": True},
        {"id": 2, "title": "Go for a walk.", "done": True},
        {"id": 3, "title": "Go to sleep.", "done": False}
    ]

@router.get("/")
def get_tasks(
    db: Session = Depends(get_db)
):
    statement = select(Task)
    result = db.execute(statement)
    tasks= result.scalars().all()
    
    return tasks
    

@router.get("/{task_id}")
def get_task_by_id(
    task_id: int,
    db:Session = Depends(get_db)
):
   statement = select(Task).where(Task.id==task_id)
   result = db.execute(statement)
   task = result.scalar_one_or_none()
   
   if task is None:
       raise HTTPException(
           status_code=404,
           detail='Task not found.'
       )
   
   return task

@router.post('/', status_code=201)
def create_task(
    task: TaskCreate,
    db:Session =Depends(get_db)
):
    if not task.title.strip():
        raise HTTPException(
            status_code =400,
            detail="Title cannot be empty or missing"
        )
    
    new_task = Task(
        title=task.title,
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    

@router.put('/{task_id}')
def update_task(
            task_id: int,
            updated_task: TaskUpdate,
            db:Session = Depends(get_db),
):
    
    statement = select(Task).where(Task.id == task_id)
    result = db.execute(statement)
    task = result.scalar_one_or_none()
    
    if task is None:
         raise HTTPException(
            status_code =404,
            detail=f'Task {task_id} not found.'
            )
    
    if updated_task.title is None and updated_task.done is None:
        raise HTTPException(
            status_code=400,
            detail='Title or done is required'
        )
    
    if updated_task.title is not None:
        if not updated_task.title.strip():
            raise HTTPException(
                        status_code =400,
                        detail="Title cannot be empty."
                    )
        task.title = updated_task.title
    
    if updated_task.done is not None:
        task.done = updated_task.done
  
    db.commit()
    return task
    
    
@router.delete('/{task_id}', status_code=204)
def delete_task(
    task_id: int,
    db:Session=Depends(get_db)
):
    statement = select(Task).where(Task.id==task_id)
    result = db.execute(statement)
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(
            status_code=404,
            detail='Task is not found.'
        )
    
    db.delete(task)
    db.commit()
    
