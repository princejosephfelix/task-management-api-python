from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.models import User, UserRole


def seed_demo_data(db: Session):
    existing = db.scalar(select(User).where(User.email == "admin@example.com"))
    if existing:
        return

    admin = User(
        email="admin@example.com",
        full_name="Demo Admin",
        password_hash=hash_password("Admin123!"),
        role=UserRole.ADMIN,
    )
    user = User(
        email="user@example.com",
        full_name="Demo User",
        password_hash=hash_password("User123!"),
        role=UserRole.USER,
    )

    db.add_all([admin, user])
    db.commit()
