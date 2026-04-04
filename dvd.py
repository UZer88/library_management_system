from media import Media

class DVD(Media):
    def __init__(self, title: str, year: int, director: str, duration_minutes: int):
        super().__init__(title, year)
        self._director = director
        self._duration_minutes = duration_minutes

    @property
    def director(self) -> str:
        return self._director

    @property
    def duration_minutes(self) -> int:
        return self._duration_minutes

    def get_loan_period_days(self) -> int:
        return 3  # DVD на 3 дня

    def get_late_fee_per_day(self) -> float:
        return 2.0  # штраф 2 рубля в день

    def __str__(self) -> str:
        return f"DVD: {self._title} — реж. {self._director} ({self._year})"