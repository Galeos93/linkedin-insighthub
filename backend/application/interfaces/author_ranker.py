from dataclasses import dataclass
from typing import List, Protocol

from domain.entities.author import AuthorPopularity
from domain.entities.post import Post


@dataclass
class AuthorRanker(Protocol):
    top_k: int = 5

    def rank(self, posts: List[Post]) -> List[AuthorPopularity]: ...
