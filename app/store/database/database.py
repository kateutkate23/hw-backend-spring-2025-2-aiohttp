from dataclasses import dataclass, field

from app.admin.models import Admin
from app.quiz.models import Theme, Question


@dataclass
class Database:
    admins: list[Admin] = field(default_factory=list)
    questions: list[Question] = field(default_factory=list)
    themes: list[Theme] = field(default_factory=list)

    @property
    def next_question_id(self) -> int:
        return len(self.questions) + 1

    @property
    def next_theme_id(self) -> int:
        return len(self.themes) + 1

    def clear(self):
        self.themes.clear()
        self.questions.clear()
