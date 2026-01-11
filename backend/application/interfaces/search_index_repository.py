from dataclasses import dataclass
from typing import List, Dict, Optional

from domain.entities.user_id import UserId

UserIndex = Dict[str, List[set]]  # token -> list of post IDs
Index = Dict[UserId, UserIndex]

@dataclass
class SearchIndexRepository:
    def save_user_index(self, user_id: UserId, index: UserIndex) -> None:
        # Implementation for saving the search index for a specific user
        pass

    def update_index(self, index: Index):
        # Implementation for updating the search index
        pass

    def get_index_by_user_id(self, user_id: UserId) -> Index | None:
        # Implementation for retrieving the search index by user ID
        pass

    def get_post_ids_by_token(self, user_id: UserId, token: str) -> Optional[list[int]]:
        # Implementation for retrieving post IDs by user ID and token
        pass

    def list_all_indexes(self) -> List[Index]:
        # Implementation for listing all search indexes
        pass
