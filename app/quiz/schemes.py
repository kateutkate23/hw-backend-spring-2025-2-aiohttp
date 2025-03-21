from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    pass


class QuestionSchema(Schema):
    pass


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema), required=True)


class ThemeIdSchema(Schema):
    theme_id = fields.Int(required=True)


class ListQuestionSchema(Schema):
    pass
