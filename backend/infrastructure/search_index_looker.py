from dataclasses import dataclass
from typing import List, Dict

from domain.entities.post import PostId
from application.interfaces.tokenizer import Tokenizer
from application.interfaces.search_index_lookup import SearchIndexLookup


@dataclass
class SimpleSearchIndexLookup(SearchIndexLookup):
    tokenizer: Tokenizer

    def lookup(
        self,
        query: str,
        index: Dict[str, set[str]],
    ) -> List[PostId]:
        tokens = self.tokenizer.tokenize(query)
        matched_post_ids = set()
        for token in tokens:
            if token in index:
                matched_post_ids.update(index[token])
        return list(matched_post_ids)
