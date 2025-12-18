from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from app.schemas.task import TaskCreate, Task, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

# -----------------------------
# Simulated in-memory database
# -----------------------------
_DB: List[Task] = []
_ID_COUNTER = 1


@router.get("/", response_model=List[Task])
async def get_tasks():
    return _DB


@router.post("/", response_model=Task, status_code=201)
async def create_task(payload: TaskCreate):
    global _ID_COUNTER

    now = datetime.utcnow()

    task = Task(
        id=_ID_COUNTER,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        priority=payload.priority,
        status="open",
        created_at=now,
        updated_at=now
    )

    _DB.append(task)
    _ID_COUNTER += 1

    return task


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in _DB:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, payload: TaskUpdate):
    for index, task in enumerate(_DB):
        if task.id == task_id:
            updated_data = task.model_dump()

            for field, value in payload.model_dump(exclude_unset=True).items():
                updated_data[field] = value

            updated_data["updated_at"] = datetime.utcnow()

            updated_task = Task(**updated_data)
            _DB[index] = updated_task

            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    for index, task in enumerate(_DB):
        if task.id == task_id:
            _DB.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

