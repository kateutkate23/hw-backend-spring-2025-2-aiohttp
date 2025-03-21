import json
import typing

from aiohttp.web_exceptions import HTTPException
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
    except HTTPException as e:
        http_status = e.status
        return error_json_response(
            http_status=http_status,
            status=HTTP_ERROR_CODES.get(http_status, "unknown error"),
            message=e.reason,
            data=json.loads(e.text),
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message="unknown server error",
            data={"error": str(e)},
        )

    return response


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
