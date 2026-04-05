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

    def search_media(self, query: str) -> List[Media]:
        """
        Ищет медиа по названию или автору (без учёта регистра)
        """
        query_lower = query.lower()
        results = []

        for media in self._media:
            # Поиск по названию
            if query_lower in media.title.lower():
                results.append(media)
                continue

            # Поиск по автору (если у медиа есть атрибут author)
            if hasattr(media, 'author') and query_lower in media.author.lower():
                results.append(media)
                continue

        return results

    def save_search_results(self, query: str, results: List[Media], filename: str = "search_results.txt") -> None:
        """Сохраняет результаты поиска в текстовый файл"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Результаты поиска по запросу: '{query}'\n")
            f.write(f"Найдено: {len(results)}\n")
            f.write("=" * 60 + "\n\n")

            for i, media in enumerate(results, 1):
                f.write(f"{i}. {media}\n")
                # Добавляем дополнительную информацию
                if hasattr(media, 'author'):
                    f.write(f"   Автор: {media.author}\n")
                if hasattr(media, 'year'):
                    f.write(f"   Год: {media.year}\n")
                if hasattr(media, 'is_loaned'):
                    f.write(f"   Статус: {'Выдано' if media.is_loaned else 'Доступно'}\n")
                f.write("\n")

        print(f"Результаты сохранены в файл: {filename}")

    def remove_media(self, title: str) -> bool:
        """Удаляет медиа из библиотеки по названию"""
        media = self.find_media_by_title(title)
        if media and media in self._media:
            # Проверяем, не выдано ли медиа
            if media.is_loaned:
                print(f"Нельзя удалить '{title}' — медиа выдано читателю")
                return False
            self._media.remove(media)
            print(f"Удалено: {title}")
            return True
        else:
            print(f"Медиа '{title}' не найдено")
            return False

    def __str__(self) -> str:
        return f"Библиотека '{self._name}': {len(self._media)} объектов, {len(self._users)} читателей"


# ----- Интерактивное меню -----
if __name__ == "__main__":
    # Создаём библиотеку и добавляем тестовые данные
    lib = Library("Центральная библиотека")

    # Добавляем медиа
    book1 = Book("1984", "Джордж Оруэлл", "978-5-17-118119-8", 1949)
    book2 = Book("Мастер и Маргарита", "Михаил Булгаков", "978-5-17-118120-4", 1967)
    book3 = Book("Преступление и наказание", "Фёдор Достоевский", "978-5-17-118122-8", 1866)
    ebook = DigitalBook("Идеальный программист", "Роберт Мартин", "978-5-17-118124-2", 2011, 8)
    dvd = DVD("Матрица", 1999, "Вачовски", 136)
    magazine = Magazine("National Geographic", 2023, 187, "NG Media")
    audiobook = AudioBook("Дюна", "Фрэнк Герберт", 2021, 480, "Иван Иванов")

    for media in [book1, book2, book3, ebook, dvd, magazine, audiobook]:
        lib.add_media(media)

    # Добавляем тестового пользователя
    user = User("Тестовый пользователь", "TEST001")
    lib.add_user(user)

    # Интерактивное меню
    while True:
        print("\n" + "=" * 50)
        print("БИБЛИОТЕЧНАЯ СИСТЕМА")
        print("=" * 50)
        print("1. Показать все медиа")
        print("2. Поиск по названию или автору")
        print("3. Показать доступные медиа")
        print("4. Выдать медиа пользователю")
        print("5. Вернуть медиа")
        print("6. Показать информацию о пользователе")
        print("7. Сохранить результаты поиска в файл")
        print("8. Удалить медиа из библиотеки")
        print("9. Выйти")

        choice = input("\nВыберите действие (1-9): ")

        if choice == "1":
            print("\n--- Все медиа ---")
            for media in lib.get_all_media():
                print(f"  {media}")
            print(f"\nВсего: {len(lib.get_all_media())}")

        elif choice == "2":
            query = input("\nВведите название или автора: ")
            results = lib.search_media(query)
            if results:
                print(f"\n--- Найдено {len(results)} результатов ---")
                for media in results:
                    print(f"  {media}")
            else:
                print("\nНичего не найдено")

        elif choice == "3":
            available = lib.get_available_media()
            print(f"\n--- Доступно {len(available)} медиа ---")
            for media in available:
                print(f"  {media}")

        elif choice == "4":
            title = input("\nВведите название медиа для выдачи: ")
            media = lib.find_media_by_title(title)
            if not media:
                print(f"Медиа '{title}' не найдено")
            else:
                if user.loan_media(media):
                    print(f"'{title}' выдано пользователю {user.name}")
                else:
                    print(f"Не удалось выдать '{title}'")

        elif choice == "5":
            title = input("\nВведите название медиа для возврата: ")
            media = lib.find_media_by_title(title)
            if not media:
                print(f"Медиа '{title}' не найдено")
            else:
                if user.return_media(media):
                    print(f"'{title}' возвращено")
                else:
                    print(f"Не удалось вернуть '{title}'")

        elif choice == "6":
            print(f"\n{user}")
            if user.loaned_media:
                print("Медиа на руках:")
                for media in user.loaned_media:
                    print(f"  - {media.title}")
            else:
                print("На руках нет медиа")

        elif choice == "7":
            query = input("\nВведите поисковый запрос для сохранения: ")
            results = lib.search_media(query)
            if results:
                filename = input("Имя файла для сохранения (по умолчанию search_results.txt): ")
                if not filename:
                    filename = "search_results.txt"
                if not filename.endswith(".txt"):
                    filename += ".txt"
                lib.save_search_results(query, results, filename)
            else:
                print("Нет результатов для сохранения")

        elif choice == "8":
            print("\n--- Удаление медиа из библиотеки ---")
            title = input("Введите название медиа для удаления: ")
            lib.remove_media(title)

        elif choice == "9":
            print("\nДо свидания!")
            break

        else:
            print("\nНеверный выбор, попробуйте снова")