from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Task model
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False
    created_at: datetime


# Request models
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None


# FastAPI app
app = FastAPI(title="To-Do List API")

# In-memory storage
tasks_db: List[Task] = []
next_id = 1


def reset_database():
    """Reset the in-memory database (useful for testing)"""
    global next_id
    tasks_db.clear()
    next_id = 1


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_create: TaskCreate):
    """Create a new task"""
    global next_id
    
    task = Task(
        id=next_id,
        title=task_create.title,
        description=task_create.description,
        done=False,
        created_at=datetime.now(timezone.utc)
    )
    tasks_db.append(task)
    next_id += 1
    
    return task


@app.get("/tasks", response_model=List[Task])
def list_tasks():
    """List all tasks"""
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a specific task by ID"""
    for task in tasks_db:
        if task.id == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task"""
    for task in tasks_db:
        if task.id == task_id:
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.done is not None:
                task.done = task_update.done
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task"""
    initial_length = len(tasks_db)
    tasks_db[:] = [task for task in tasks_db if task.id != task_id]
    
    if len(tasks_db) == initial_length:
        raise HTTPException(status_code=404, detail="Task not found")
