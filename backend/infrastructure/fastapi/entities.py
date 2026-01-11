from dataclasses import dataclass, field

from domain.entities.post import PostId


@dataclass
class PostRequest:
    author: str
    profileUrl: str
    authorImage: str
    authorHeadline: str
    timestamp: str
    text: str
    postUrl: str
    meta: dict
    postImage: str
