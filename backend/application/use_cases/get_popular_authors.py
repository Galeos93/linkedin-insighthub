from dataclasses import dataclass
from typing import List

from domain.entities.post import Post
from domain.entities.user_id import UserId
from domain.entities.author import AuthorPopularity
from domain.interfaces.post_repository import PostRepository
from infrastructure.simple_author_ranker import AuthorRanker


@dataclass
class GetPopularAuthors:
    author_ranker: AuthorRanker
    post_repository: PostRepository

    def execute(self, user_id: UserId) -> List[AuthorPopularity]:
        posts = self.post_repository.get_posts_by_user_id(user_id)
        return self.author_ranker.rank(posts)
