from abc import ABC, abstractmethod
from typing import List, Dict

from domain.entities.user_id import UserId
from domain.entities.search import Post
from application.interfaces.tokenizer import Tokenizer

UserIndex = Dict[str, List[set]]  # token -> list of post IDs


class SearchIndexBuilder(ABC):
    @abstractmethod
    def build_index(self, posts: List[Post], tokenizer: Tokenizer) -> UserIndex:
        pass
