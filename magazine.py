from media import Media

class Magazine(Media):
    def __init__(self, title: str, year: int, issue_number: int, publisher: str):
        super().__init__(title, year)
        self._issue_number = issue_number
        self._publisher = publisher

    @property
    def issue_number(self) -> int:
        return self._issue_number

    @property
    def publisher(self) -> str:
        return self._publisher

    def get_loan_period_days(self) -> int:
        return 7  # журналы на 7 дней

    def get_late_fee_per_day(self) -> float:
        return 1.0  # штраф 1 рубль в день

    def __str__(self) -> str:
        return f"Журнал: {self._title} №{self._issue_number} ({self._year})"