from dataclasses import dataclass

from domain.entities.post import Post, PostProjection
from domain.entities.user_id import UserId
from domain.interfaces.post_repository import PostRepository
from application.interfaces.post_projector import PostProjector


@dataclass
class ComputeProjection:
    post_repository: PostRepository
    post_projector: PostProjector

    def compute(self, user_id: UserId) -> list[PostProjection]:
        posts = self.post_repository.get_posts_by_user_id(user_id)
        projections = self.post_projector.project(posts=posts)  # type: ignore hel
        return projections
