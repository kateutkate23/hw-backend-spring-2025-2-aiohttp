import hashlib

from aiohttp_apispec import request_schema, response_schema

from app.admin.schemes import AdminSchema
from app.web.app import View
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

        return json_response(
            data={
                "id": admin.id,
                "email": admin.email,
            }
        )


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
