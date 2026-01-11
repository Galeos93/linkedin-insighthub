from dataclasses import dataclass, field
from typing import Dict, Optional

from application.interfaces.search_index_repository import (
    SearchIndexRepository, UserIndex, Index
)
from domain.entities.user_id import UserId


@dataclass
class InMemorySearchIndexRepository(SearchIndexRepository):
    _storage: Index = field(default_factory=dict)

    def save_user_index(self, user_id: UserId, index: UserIndex) -> None:
        """Save or overwrite the index for a specific user."""
        self._storage[user_id] = index

    def update_index(self, index: Index) -> None:
        """Update the storage with the provided index data."""
        for user_id, user_index in index.items():
            self._storage[user_id] = user_index

    def get_index_by_user_id(self, user_id: UserId) -> Optional[UserIndex]:
        """Retrieve the index for a given user, or None if not exists."""
        return self._storage.get(user_id)

    def get_post_ids_by_token(self, user_id: UserId, token: str) -> Optional[list[int]]:
        """Retrieve the list of post IDs for a given user and token, or None if not exists."""
        user_index = self._storage.get(user_id)
        if user_index is None:
            return None
        return user_index.get(token)

    def list_all_indexes(self) -> Dict[UserId, UserIndex]:
        """Return all user indexes (for debugging or admin purposes)."""
        return dict(self._storage)  # return a shallow copy
