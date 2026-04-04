from typing import List
from media import Media

class User:
    def __init__(self, name: str, user_id: str):
        self._name = name
        self._user_id = user_id
        self._loaned_media: List[Media] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def loaned_media(self) -> List[Media]:
        return self._loaned_media.copy()

    def can_loan(self, media: Media) -> bool:
        """Обычный пользователь: максимум 3 объекта"""
        return len(self._loaned_media) < 3

    def loan_media(self, media: Media) -> bool:
        if not self.can_loan(media):
            print(f"{self._name}: достигнут лимит (3)")
            return False
        if not media.loan():
            print(f"'{media.title}' уже выдано")
            return False
        self._loaned_media.append(media)
        print(f"{self._name} взял '{media.title}'")
        return True

    def return_media(self, media: Media) -> bool:
        if media not in self._loaned_media:
            print(f"{self._name} не брал '{media.title}'")
            return False
        media.return_media()
        self._loaned_media.remove(media)
        print(f"{self._name} вернул '{media.title}'")
        return True

    def __str__(self) -> str:
        return f"{self._name} (ID: {self._user_id}) — на руках: {len(self._loaned_media)}"


class PremiumUser(User):
    def __init__(self, name: str, user_id: str, membership_level: str = "gold"):
        super().__init__(name, user_id)
        self._membership_level = membership_level

    @property
    def membership_level(self) -> str:
        return self._membership_level

    def can_loan(self, media: Media) -> bool:
        """Премиум-пользователь: до 10 объектов"""
        return len(self._loaned_media) < 10

    def __str__(self) -> str:
        return super().__str__() + f" [Премиум: {self._membership_level}]"