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
def get_task_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(
        status_code = 404,
        detail = f"Task {task_id} not found."
    )
@router.post('/', status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(
            status_code =400,
            detail="Title cannot be empty or missing"
        )
    new_id = max(task["id"] for task in tasks)+1
    
    new_task ={
        "id": new_id,
        "title": task.title,
        "done": False
    }
    
    tasks.append(new_task)
    return new_task

@router.put('/{task_id}')
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task['id'] == task_id:
            if task_update.title is None and task_update.done is None:
                raise HTTPException(
                    status_code = 400,
                    detail = "At least one field must be provided."
                )
                
            if task_update.title is not None:
                if not task_update.title.strip():
                    raise HTTPException(
                        status_code = 400,
                        detail="Ttile cannot be empty."
                    )
                task["title"] = task_update.title
                
            if task_update.done is not None:
                task["done"] = task_update.done
            
            return task
    
    raise HTTPException(
    status_code =404,
    detail=f'Task {task_id} not found.'
    )
        
@router.delete('/{task_id}', status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(index)
            return
        
    raise HTTPException(
     status_code=404,
     detail=f'Task {task_id} not found.'
    )