from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

from fastapi import Depends

from domain.entities.post import PostId, UserId
from application.use_cases.search_posts import SearchPosts
from infrastructure.fastapi.common import get_anonymous_user


class SearchPostsAPIBase(ABC):
    @abstractmethod
    async def search_posts(self, query: str, user_id: UserId) -> List[PostId]:
        pass


@dataclass
class SearchPostsAPIImpl(SearchPostsAPIBase):
    search_posts_use_case: SearchPosts

    async def search_posts(self, query: str, user_id: UserId = Depends(get_anonymous_user)) -> List[PostId]:
        return self.search_posts_use_case.execute(query=query, user_id=user_id)