from dataclasses import dataclass

from domain.entities.post import Post, PostId
from domain.entities.user_id import UserId


@dataclass
class PostRepository:
    def get_post(self, post_id: PostId) -> Post | None:
        pass

    def get_posts(self) -> list[Post]:
        pass

    def get_post_by_id(self, post_id: PostId) -> Post | None:
        pass

    def get_posts_by_ids(self, post_ids: list[PostId]) -> list[Post]:
        pass

    def get_posts_by_user_id(self, user_id: UserId) -> list[Post]:
        pass

    def get_posts_by_user_id_and_ids(self, user_id: UserId, post_ids: list[PostId]) -> list[Post]:
        pass

    def add_posts(self, posts: list[Post]) -> None:
        pass
