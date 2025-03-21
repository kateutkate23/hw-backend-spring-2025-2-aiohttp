from marshmallow import Schema, fields
from app.web.schemes import OkResponseSchema


class AdminSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
