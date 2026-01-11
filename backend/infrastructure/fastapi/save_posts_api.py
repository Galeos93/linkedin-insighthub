from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, asdict
from uuid import uuid4

from fastapi import Body, Depends

from application.use_cases.save_posts import SavePostsUseCase
from domain.entities.post import Post
from domain.entities.user_id import UserId
from infrastructure.fastapi.entities import PostRequest
from infrastructure.fastapi.common import get_anonymous_user


class SavePostsAPIBase(ABC):
    @abstractmethod
    async def save_posts(self, user_id: UserId = Depends(get_anonymous_user), posts: List[PostRequest] = Body(...)) -> None:
        pass


@dataclass
class SavePostsAPIImpl(SavePostsAPIBase):
    save_posts_use_case: SavePostsUseCase

    async def save_posts(self, user_id: UserId = Depends(get_anonymous_user), posts: List[PostRequest] = Body(...)) -> None:
        # "zip" user id and post request to create Post entities
        posts = [
            Post(
                userId=user_id,
                id=uuid4().hex,
                **asdict(post_request)
            ) for post_request in posts
        ]

        return self.save_posts_use_case.execute(posts)
