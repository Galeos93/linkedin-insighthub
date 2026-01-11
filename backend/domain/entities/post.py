from dataclasses import dataclass, field
from typing import NewType, Optional

from domain.entities.user_id import UserId


PostId = NewType("PostId", str)


@dataclass
class Post:
    author: str
    profileUrl: str
    authorImage: str
    authorHeadline: str
    timestamp: str
    text: str
    postUrl: str
    meta: dict
    postImage: str
    userId: UserId
    id: PostId


@dataclass(frozen=True)
class KeywordRelevance:
    keyword: str
    score: float


@dataclass(frozen=True)
class PostProjection:
    post_id: PostId
    x: float
    y: float
    keywords: list[KeywordRelevance]
