from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.database.models import Task, TaskPriority, TaskStatus


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

    def list(
        self,
        owner_id: int | None,
        page: int,
        page_size: int,
        status: TaskStatus | None,
        priority: TaskPriority | None,
        search: str | None,
        sort_by: str,
        sort_order: str,
    ):
        filters = []

        if owner_id is not None:
            filters.append(Task.owner_id == owner_id)
        if status is not None:
            filters.append(Task.status == status)
        if priority is not None:
            filters.append(Task.priority == priority)
        if search:
            pattern = f"%{search}%"
            filters.append(
                or_(
                    Task.title.ilike(pattern),
                    Task.description.ilike(pattern),
                )
            )

        count_query = select(func.count()).select_from(Task).where(*filters)
        total = self.db.scalar(count_query) or 0

        sort_column = {
            "id": Task.id,
            "title": Task.title,
            "created_at": Task.created_at,
            "updated_at": Task.updated_at,
        }.get(sort_by, Task.created_at)

        order_expression = (
            sort_column.desc() if sort_order.lower() == "desc" else sort_column.asc()
        )

        query = (
            select(Task)
            .where(*filters)
            .order_by(order_expression)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        items = list(self.db.scalars(query).all())
        return items, total
