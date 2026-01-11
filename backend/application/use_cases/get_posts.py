from dataclasses import dataclass

from domain.interfaces.post_repository import PostRepository
from domain.entities.post import Post, PostId
from domain.entities.user_id import UserId

from typing import Optional


@dataclass
class GetPostsUseCase:
    post_repository: PostRepository

    def execute(
        self,
        user_id: UserId,
        post_ids: Optional[list[PostId]]
    ) -> list[Post]:
        if post_ids is None:
            return self.post_repository.get_posts_by_user_id(user_id=user_id)

        return self.post_repository.get_posts_by_user_id_and_ids(
            user_id=user_id,
            post_ids=post_ids
        )
