from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

from fastapi import Query, Depends

from application.use_cases.get_posts import GetPostsUseCase
from domain.entities.post import Post, PostId
from domain.entities.user_id import UserId
from infrastructure.fastapi.common import get_anonymous_user


class GetPostsAPIBase(ABC):
    @abstractmethod
    async def get_posts(self, user_id: UserId, ids: Optional[List[PostId]] = Query(None)) -> List[Post]:
        pass

    @abstractmethod
    async def get_post(self, user_id: UserId, id: PostId) -> Optional[Post]:
        pass


@dataclass
class GetPostsAPIImpl(GetPostsAPIBase):
    get_posts_use_case: GetPostsUseCase

    async def get_posts(self, user_id: UserId = Depends(get_anonymous_user), ids: Optional[List[PostId]] = Query(None)) -> List[Post]:
        return self.get_posts_use_case.execute(
            user_id=user_id,
            post_ids=ids if ids else None
        )

    async def get_post(self, user_id: UserId = Depends(get_anonymous_user), id: PostId = Query(...)) -> Optional[Post]:
        posts = self.get_posts_use_case.execute(
            user_id=user_id,
            post_ids=[id]
        )
        return posts[0] if posts else None
