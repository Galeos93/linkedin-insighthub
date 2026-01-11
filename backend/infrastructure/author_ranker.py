from dataclasses import dataclass
from typing import List, Protocol
from collections import Counter
from backend.domain.entities.author import AuthorPopularity
from backend.domain.entities.post import Post

class AuthorRanker(Protocol):
    def rank(self, posts: List[Post]) -> List[AuthorPopularity]: ...

@dataclass
class SimpleAuthorRanker:
    def rank(self, posts: List[Post]) -> List[AuthorPopularity]:
        counts = Counter(post.author for post in posts)
        popular = [AuthorPopularity(author=a, post_count=c) for a, c in counts.items()]
        return sorted(popular, key=lambda ap: ap.post_count, reverse=True)
