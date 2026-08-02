from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.task import Task
def seed_database():
    db = SessionLocal()
    
    try:
        statement = select(Task)
        result = db.execute(statement)
        tasks = result.scalars().all()
        
        if not tasks:
            task1 = Task(title="Go to church", done=False)
            task2 = Task(title="Play league of legends", done=False)
            task3 = Task(title="Play basketball", done=False)
        
            db.add_all([task1,task2,task3])
        
            db.commit()
    finally:
        db.close()