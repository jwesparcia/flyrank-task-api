from fastapi import APIRouter

router = APIRouter(
    prefix = "/tasks",
    tags = ["Tasks"]
)

@router.get("/")
def get_tasks():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }