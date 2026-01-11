from dataclasses import dataclass
from typing import List, Protocol
from collections import Counter

from application.interfaces.author_ranker import AuthorRanker
from domain.entities.author import AuthorPopularity
from domain.entities.post import Post


@dataclass
class SimpleAuthorRanker(AuthorRanker):
    def rank(self, posts: List[Post]) -> List[AuthorPopularity]:
        counts = Counter(post.author for post in posts)
        popular = [AuthorPopularity(author=a, post_count=c) for a, c in counts.items()]
        return sorted(popular, key=lambda ap: ap.post_count, reverse=True)[:self.top_k]
