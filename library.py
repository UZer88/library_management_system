from typing import List, Optional
from datetime import datetime, timedelta
from media import Media
from user import User, PremiumUser
from book import Book
from digital_book import DigitalBook
from magazine import Magazine
from audio_book import AudioBook
from dvd import DVD


class Library:
    def __init__(self, name: str):
        self._name = name
        self._media: List[Media] = []
        self._users: List[User] = []

    @property
    def name(self) -> str:
        return self._name

    def add_media(self, media: Media) -> None:
        if media not in self._media:
            self._media.append(media)
            print(f"Добавлено: {media.title}")

    def add_user(self, user: User) -> None:
        if user not in self._users:
            self._users.append(user)
            print(f"Зарегистрирован пользователь: {user.name}")

    def find_media_by_title(self, title: str) -> Optional[Media]:
        for media in self._media:
            if media.title.lower() == title.lower():
                return media
        return None

    def find_user_by_id(self, user_id: str) -> Optional[User]:
        for user in self._users:
            if user.user_id == user_id:
                return user
        return None

    def get_available_media(self) -> List[Media]:
        return [media for media in self._media if not media.is_loaned]

    def get_media_by_author(self, author: str) -> List[Media]:
        result = []
        for media in self._media:
            if hasattr(media, 'author') and author.lower() in media.author.lower():
                result.append(media)
        return result

    def get_most_popular_media(self) -> Optional[Media]:
        if not self._media:
            return None
        return max(self._media, key=lambda media: media.loan_count)

    def calculate_fine(self, media: Media, loan_date: datetime, return_date: datetime) -> float:
        loan_period = media.get_loan_period_days()
        due_date = loan_date + timedelta(days=loan_period)
        if return_date <= due_date:
            return 0.0
        days_late = (return_date - due_date).days
        fine_per_day = media.get_late_fee_per_day()
        return days_late * fine_per_day

    def get_all_media(self) -> List[Media]:
        return self._media

    def __str__(self) -> str:
        return f"Библиотека '{self._name}': {len(self._media)} объектов, {len(self._users)} читателей"


# ----- Тестирование -----
if __name__ == "__main__":
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ БИБЛИОТЕКИ")
    print("=" * 50)

    lib = Library("Центральная библиотека")
    print(f"\nСоздана библиотека: {lib.name}")

    print("\n--- Добавление медиа ---")
    book1 = Book("1984", "Джордж Оруэлл", "978-5-17-118119-8", 1949)
    book2 = Book("Мастер и Маргарита", "Михаил Булгаков", "978-5-17-118120-4", 1967)
    ebook = DigitalBook("Python на практике", "Марк Лутц", "978-5-17-118121-1", 2020, 15)
    magazine = Magazine("National Geographic", 2023, 187, "NG Media")
    audiobook = AudioBook("Дюна", "Фрэнк Герберт", 2021, 480, "Иван Иванов")
    dvd = DVD("Матрица", 1999, "Вачовски", 136)

    lib.add_media(book1)
    lib.add_media(book2)
    lib.add_media(ebook)
    lib.add_media(magazine)
    lib.add_media(audiobook)
    lib.add_media(dvd)

    print("\n--- Добавление пользователей ---")
    user1 = User("Анна", "U001")
    user2 = PremiumUser("Иван", "U002", "gold")
    lib.add_user(user1)
    lib.add_user(user2)

    print(f"\n{lib}")
    print(f"Всего медиа: {len(lib.get_all_media())}")
    print(f"Доступно: {len(lib.get_available_media())}")

    print("\n--- Список всех медиа ---")
    for media in lib.get_all_media():
        print(f"  {media}")

    print("\n--- Сроки выдачи и штрафы ---")
    for media in [book1, magazine, audiobook, dvd]:
        print(f"  {media.title}: срок {media.get_loan_period_days()} дней, штраф {media.get_late_fee_per_day()} руб/день")

    print("\n--- Выдача медиа ---")
    user1.loan_media(book1)
    user1.loan_media(dvd)
    user2.loan_media(ebook)
    user2.loan_media(book2)

    print(f"\nДоступно после выдач: {len(lib.get_available_media())}")
    for media in lib.get_available_media():
        print(f"  {media.title}")

    popular = lib.get_most_popular_media()
    if popular:
        print(f"\nСамое популярное: {popular.title} (выдано {popular.loan_count} раз)")

    print("\n--- Возврат ---")
    user1.return_media(book1)

    print(f"\n{lib}")
    print(f"Книги Анны: {[m.title for m in user1.loaned_media]}")
    print(f"Книги Ивана: {[m.title for m in user2.loaned_media]}")

    print("\n--- Тест штрафа за просрочку ---")
    loan_date = datetime.now() - timedelta(days=10)
    return_date = datetime.now()
    fine = lib.calculate_fine(dvd, loan_date, return_date)
    print(f"DVD выдан на 3 дня, просрочка на 7 дней: штраф = {fine} руб")

    print("\n" + "=" * 50)
    print("ТЕСТ ЗАВЕРШЁН")
    print("=" * 50)