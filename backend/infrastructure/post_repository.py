from dataclasses import dataclass, field
from typing import Dict, List, Optional

from domain.interfaces.post_repository import PostRepository
from domain.entities.post import Post, PostId
from domain.entities.user_id import UserId


@dataclass
class InMemoryPostRepository(PostRepository):
    _by_post_id: Dict[PostId, Post] = field(default_factory=dict)
    _by_user_id: Dict[UserId, List[Post]] = field(default_factory=dict)

    def add_post(self, post: Post) -> None:
        self._by_post_id[post.id] = post

        if post.userId not in self._by_user_id:
            self._by_user_id[post.userId] = []
        self._by_user_id[post.userId].append(post)

    def add_posts(self, posts):
        for post in posts:
            self.add_post(post)

    def get_post_by_id(self, post_id: PostId) -> Optional[Post]:
        return self._by_post_id.get(post_id)

    def get_posts_by_ids(self, post_ids: List[PostId]) -> List[Post]:
        return [self._by_post_id[pid] for pid in post_ids if pid in self._by_post_id]

    def get_posts_by_user_id(self, user_id: UserId) -> List[Post]:
        return self._by_user_id.get(user_id, [])

    def get_posts_by_user_id_and_ids(self, user_id: UserId, post_ids: List[PostId]) -> List[Post]:
        user_posts = self._by_user_id.get(user_id, [])
        user_post_ids = {post.id for post in user_posts}
        filtered_post_ids = [pid for pid in post_ids if pid in user_post_ids]
        return [self._by_post_id[pid] for pid in filtered_post_ids]

    def get_posts(self) -> List[Post]:
        return list(self._by_post_id.values())

