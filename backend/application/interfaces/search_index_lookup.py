from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

from domain.entities.user_id import UserId
from domain.entities.post import PostId
from application.interfaces.tokenizer import Tokenizer


@dataclass
class SearchIndexLookup(ABC):
    tokenizer: Tokenizer

    @abstractmethod
    def lookup(
        self,
        query: str,
        index: Dict[str, set[str]],
    ) -> List[PostId]:
        pass
