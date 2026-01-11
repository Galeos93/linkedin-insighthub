from dataclasses import dataclass

from domain.interfaces.post_repository import PostRepository
from domain.entities.post import Post
from domain.entities.user_id import UserId

from typing import Optional


@dataclass
class SavePostsUseCase:
    post_repository: PostRepository

    def execute(
        self,
        posts: Optional[list[Post]]
    ) -> None:
        if posts is None:
            return []
        return self.post_repository.add_posts(posts)
