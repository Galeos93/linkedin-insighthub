from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

from domain.entities.search import SearchResult, Post


class SnippetBuilder(ABC):
    @abstractmethod
    def build(self, matches: List[Tuple[str, float]], tokens: List[str]) -> List[SearchResult]:
        pass
