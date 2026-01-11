from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorPopularity:
    author: str
    post_count: int
