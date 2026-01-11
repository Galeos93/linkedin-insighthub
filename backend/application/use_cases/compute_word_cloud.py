from dataclasses import dataclass

from domain.entities.user_id import UserId
from domain.interfaces.post_repository import PostRepository
from application.interfaces.post_wordcloud_projector import PostWordCloudProjector


@dataclass
class ComputeWordCloud:
    post_repository: PostRepository
    post_wordcloud_projector: PostWordCloudProjector

    def compute(self, user_id: UserId) -> bytes:
        posts = self.post_repository.get_posts_by_user_id(user_id)
        worldcloud = self.post_wordcloud_projector.compute_word_cloud(posts)
        return worldcloud
