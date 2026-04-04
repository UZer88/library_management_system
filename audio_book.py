from media import Media

class AudioBook(Media):
    def __init__(self, title: str, author: str, year: int, duration_minutes: int, narrator: str):
        super().__init__(title, year)
        self._author = author
        self._duration_minutes = duration_minutes
        self._narrator = narrator

    @property
    def author(self) -> str:
        return self._author

    @property
    def duration_minutes(self) -> int:
        return self._duration_minutes

    @property
    def narrator(self) -> str:
        return self._narrator

    def get_loan_period_days(self) -> int:
        return 21  # аудиокниги на 3 недели

    def get_late_fee_per_day(self) -> float:
        return 0.75

    def __str__(self) -> str:
        return f"Аудиокнига: {self._title} — {self._author} (читает {self._narrator}, {self._duration_minutes} мин)"