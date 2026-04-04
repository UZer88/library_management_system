from book import Book

class DigitalBook(Book):
    def __init__(self, title: str, author: str, isbn: str, year: int, file_size_mb: int):
        super().__init__(title, author, isbn, year)
        self._file_size_mb = file_size_mb

    @property
    def file_size_mb(self) -> int:
        return self._file_size_mb

    def download_link(self) -> str:
        return f"https://library.com/download/{self.isbn}"

    def loan(self) -> bool:
        # Электронные книги всегда доступны
        self._loan_count += 1
        return True

    def get_loan_period_days(self) -> int:
        return 21  # электронные книги на 3 недели

    def get_late_fee_per_day(self) -> float:
        return 0.0  # за электронные книги штрафа нет

    def __str__(self) -> str:
        return super().__str__() + f" [электронная, {self._file_size_mb} МБ]"