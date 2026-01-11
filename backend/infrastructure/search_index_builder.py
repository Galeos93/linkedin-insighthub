from collections import defaultdict, Counter
from typing import List, Set
from domain.entities.search import Post

from application.interfaces.search_index_builder import UserIndex, SearchIndexBuilder
from application.interfaces.tokenizer import Tokenizer


class InMemorySearchIndexBuilder(SearchIndexBuilder):
    def build_index(self, posts: List[Post], tokenizer: Tokenizer) -> UserIndex:
        index: UserIndex = defaultdict(set)

        for post in posts:
            tokens = tokenizer.tokenize(post.text)
            for token in set(tokens):
                index[token].add(post.id)

        return index
