from book import Book
from digital_book import DigitalBook
from magazine import Magazine
from audio_book import AudioBook
from dvd import DVD
from user import User, PremiumUser
from library import Library
from datetime import datetime, timedelta

lib = Library("Медиатека")

book = Book("1984", "Оруэлл", "123", 1949)
ebook = DigitalBook("Python", "Лутц", "456", 2020, 15)
magazine = Magazine("National Geographic", 2023, 187, "NG Media")
audiobook = AudioBook("Дюна", "Фрэнк Герберт", 2021, 480, "Иван Иванов")
dvd = DVD("Матрица", 1999, "Вачовски", 136)

for media in [book, ebook, magazine, audiobook, dvd]:
    lib.add_media(media)

user = User("Анна", "U001")
lib.add_user(user)

print("\n--- Выдача DVD ---")
user.loan_media(dvd)

loan_date = datetime.now() - timedelta(days=8)
return_date = datetime.now()
fine = lib.calculate_fine(dvd, loan_date, return_date)
print(f"Просрочка на 5 дней. Штраф: {fine} руб")

print("\n--- Доступные медиа ---")
available = lib.get_available_media()
print([m.title for m in available])