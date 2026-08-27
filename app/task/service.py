from math import ceil

from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.database.models import Task, TaskPriority, TaskStatus, User, UserRole
from app.task.repository import TaskRepository
from app.task.schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.tasks = TaskRepository(db)

    def _get_or_404(self, task_id: int) -> Task:
        task = self.tasks.get(task_id)
        if not task:
            raise AppException(404, "Task not found", "task_not_found")
        return task

    @staticmethod
    def _can_access(task: Task, user: User) -> bool:
        return user.role == UserRole.ADMIN or task.owner_id == user.id

    def create(self, data: TaskCreate, user: User) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            priority=data.priority,
            status=TaskStatus.TODO,
            owner_id=user.id,
        )
        return self.tasks.create(task)

    def get(self, task_id: int, user: User) -> Task:
        task = self._get_or_404(task_id)
        if not self._can_access(task, user):
            raise AppException(403, "You cannot access this task", "forbidden")
        return task

    def update(self, task_id: int, data: TaskUpdate, user: User) -> Task:
        task = self.get(task_id, user)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        self.tasks.db.commit()
        self.tasks.db.refresh(task)
        return task

    def delete(self, task_id: int, user: User) -> None:
        task = self.get(task_id, user)
        self.tasks.delete(task)

    def list(
        self,
        user: User,
        page: int,
        page_size: int,
        status: TaskStatus | None,
        priority: TaskPriority | None,
        search: str | None,
        sort_by: str,
        sort_order: str,
    ):
        owner_id = None if user.role == UserRole.ADMIN else user.id

        items, total = self.tasks.list(
            owner_id=owner_id,
            page=page,
            page_size=page_size,
            status=status,
            priority=priority,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": ceil(total / page_size) if total else 0,
        }
