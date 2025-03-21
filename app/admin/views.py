import hashlib

from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import get_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.schemes import OkResponseSchema
from app.web.utils import error_json_response, json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = self.request["data"]
        email = data["email"]
        password = data["password"]

        admin = await self.store.admins.get_by_email(email)
        if not admin:
            return error_json_response(
                http_status=403,
                status="forbidden",
                message="email or password is incorrect"
            )

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password != admin.password:
            return error_json_response(
                http_status=403,
                status="forbidden",
                message="email or password is incorrect"
            )

        session = await get_session(self.request)
        session["admin_id"] = admin.id
        session["admin_email"] = admin.email

        return json_response(
            data={
                "id": admin.id,
                "email": admin.email,
            }
        )


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        admin = self.request.admin
        return json_response(
            data={
                "id": admin.id,
                "email": admin.email,
            }
        )
