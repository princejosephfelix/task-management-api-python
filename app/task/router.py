from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.database.models import TaskPriority, TaskStatus, User
from app.task.schemas import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.task.service import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    data: TaskCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return TaskService(db).create(data, current_user)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    status_filter: Annotated[
    TaskStatus | None,
    Query(alias="status"),
                            ] = None,
    priority: TaskPriority | None = None,
    search: Annotated[
    str | None,
    Query(max_length=100),
                    ] = None,
    sort_by: Annotated[str, Query()] = "created_at",
    sort_order: Annotated[str, Query(pattern="^(asc|desc)$")] = "desc",
):
    return TaskService(db).list(
        current_user,
        page,
        page_size,
        status_filter,
        priority,
        search,
        sort_by,
        sort_order,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return TaskService(db).get(task_id, current_user)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return TaskService(db).update(task_id, data, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    TaskService(db).delete(task_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
