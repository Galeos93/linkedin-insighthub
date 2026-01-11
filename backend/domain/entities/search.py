from dataclasses import dataclass

@dataclass(frozen=True)
class Post:
    id: str
    text: str

@dataclass(frozen=True)
class SearchResult:
    post_id: str
    score: float
    snippet: str
