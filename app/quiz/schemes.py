from marshmallow import Schema, fields, validates_schema, ValidationError


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema), required=True)

    @validates_schema
    def validate_answers(self, data, **kwargs):
        answers = data["answers"]
        if len(answers) <= 1:
            raise ValidationError("question must have more than one answer", "answers")
        correct_answers = [ans for ans in answers if ans["is_correct"]]
        if not correct_answers:
            raise ValidationError("at least one answer must be correct", "answers")
        if len(correct_answers) > 1:
            raise ValidationError("only one answer can be correct", "answers")


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema), required=True)


class ThemeIdSchema(Schema):
    theme_id = fields.Int(required=True)


class ListQuestionSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema), required=True)
