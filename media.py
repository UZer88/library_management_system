from abc import ABC, abstractmethod

class Media(ABC):
    """Абстрактный базовый класс для всех медиа-объектов"""

    def __init__(self, title: str, year: int):
        self._title = title
        self._year = year
        self._is_loaned = False
        self._loan_count = 0

    @property
    def title(self) -> str:
        return self._title

    @property
    def year(self) -> int:
        return self._year

    @property
    def is_loaned(self) -> bool:
        return self._is_loaned

    @property
    def loan_count(self) -> int:
        return self._loan_count

    def loan(self) -> bool:
        if self._is_loaned:
            return False
        self._is_loaned = True
        self._loan_count += 1
        return True

    def return_media(self) -> None:
        self._is_loaned = False

    @abstractmethod
    def get_loan_period_days(self) -> int:
        """Срок выдачи в днях (разный для разных типов)"""
        pass

    @abstractmethod
    def get_late_fee_per_day(self) -> float:
        """Штраф за просрочку в день"""
        pass

    def __str__(self) -> str:
        return f"{self._title} ({self._year})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Media):
            return False
        return self._title == other._title and self._year == other._year