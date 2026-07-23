from fastapi import FastAPI
from app.api.routes.task_routes import router as task_router
from app.api.routes.health_routes import router as health_router
app = FastAPI()


@app.get("/")
async def root():
    return {"name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"]}

app.include_router(task_router)
app.include_router(health_router)