from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import ThemeSchema, QuestionSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response, error_json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        title = self.data["title"]

        theme = await self.store.quizzes.get_theme_by_title(title)
        if theme:
            return error_json_response(
                http_status=409,
                status="conflict",
                message="theme already exists",
            )

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        themes = await self.store.quizzes.list_themes()

        return json_response(
            data={
                "themes": [{"id": theme.id, "title": theme.title} for theme in themes],
            }
        )


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers = self.data["answers"]

        question = await self.store.quizzes.get_question_by_title(title)
        if question:
            return error_json_response(
                http_status=409,
                status="conflict",
                message="question already exists",
            )

        theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme:
            return error_json_response(
                http_status=404,
                status="not_found",
                message="theme does not exist",
            )

        question = await self.store.quizzes.create_question(title, theme_id, answers)
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
