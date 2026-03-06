from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src import models, schemas
from src.auth import get_current_user
from fastapi import HTTPException


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    new_task = models.Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    # Admin can see all tasks
    if current_user.role == "admin":
        tasks = db.query(models.Task).all()

    # Normal users see only their tasks
    else:
        tasks = db.query(models.Task).filter(
            models.Task.user_id == current_user.id
        ).all()

    return tasks

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Authorization check
    if current_user.role != "admin" and db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if task.title is not None:
        db_task.title = task.title

    if task.description is not None:
        db_task.description = task.description

    if task.status is not None:
        db_task.status = task.status

    db.commit()
    db.refresh(db_task)

    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Authorization check
    if current_user.role != "admin" and db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}