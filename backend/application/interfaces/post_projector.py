from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.post import PostProjection, Post

@dataclass
class PostProjector(ABC):
    @abstractmethod
    def project(self, posts: list[Post]) -> list[PostProjection]:
        pass
