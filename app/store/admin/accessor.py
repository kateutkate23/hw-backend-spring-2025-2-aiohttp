import hashlib
import typing

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        admin_config = app.config.admin

        email = admin_config.email
        password = admin_config.password

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        app.database.admins.append(Admin(1, email, hashed_password))

    async def get_by_email(self, email: str) -> Admin | None:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin

    async def get_by_id(self, id_: int) -> Admin | None:
        for admin in self.app.database.admins:
            if admin.id == id_:
                return admin

    async def create_admin(self, email: str, password: str) -> Admin:
        existing_admin = await self.get_by_email(email)
        if existing_admin:
            raise ValueError(f"Admin with email {email} already exists")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        admin = Admin(len(self.app.database.admins) + 1, email, hashed_password)
        self.app.database.admins.append(admin)
        return admin
