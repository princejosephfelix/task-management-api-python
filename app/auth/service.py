from sqlalchemy.orm import Session

from app.auth.repository import UserRepository
from app.auth.schemas import RegisterRequest
from app.core.exceptions import AppException
from app.core.security import create_access_token, hash_password, verify_password
from app.database.models import User, UserRole


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def register(self, request: RegisterRequest) -> User:
        if self.users.get_by_email(request.email):
            raise AppException(409, "Email is already registered", "email_exists")

        user = User(
            email=request.email,
            full_name=request.full_name,
            password_hash=hash_password(request.password),
            role=UserRole.USER,
        )
        return self.users.create(user)

    def authenticate(self, email: str, password: str) -> str:
        user = self.users.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise AppException(401, "Invalid email or password", "invalid_credentials")

        return create_access_token(str(user.id), user.role.value)
