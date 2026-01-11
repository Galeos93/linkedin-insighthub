from abc import ABC, abstractmethod
from dataclasses import dataclass
from domain.entities.post import Post

@dataclass
class PostWordCloudProjector(ABC):
    @abstractmethod
    def compute_word_cloud(posts: list[Post]) -> bytes:
        """
        Compute a word cloud for the given posts.
        Returns an image file in bytes.
        """
        pass
