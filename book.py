from media import Media

class Book(Media):
    def __init__(self, title: str, author: str, isbn: str, year: int):
        super().__init__(title, year)
        self._author = author
        self._isbn = isbn

    @property
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> str:
        return self._isbn

    def get_loan_period_days(self) -> int:
        return 14  # книги на 2 недели

    def get_late_fee_per_day(self) -> float:
        return 0.5  # 50 копеек в день

    def __str__(self) -> str:
        return f"{self._title} — {self._author} ({self._year})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return False
        return self._isbn == other._isbn