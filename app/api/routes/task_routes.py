from fastapi import APIRouter, HTTPException

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
def get_tasks():
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