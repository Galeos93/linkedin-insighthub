from dataclasses import dataclass
from typing import List

from domain.interfaces.post_repository import PostRepository
from domain.entities.user_id import UserId
from domain.entities.search import SearchResult
from domain.entities.post import PostId
from application.interfaces.search_index_lookup import SearchIndexLookup
from application.interfaces.search_index_repository import SearchIndexRepository
from application.interfaces.search_index_builder import SearchIndexBuilder
from application.interfaces.tokenizer import Tokenizer


@dataclass
class SearchPosts:
    index_lookup: SearchIndexLookup
    index_repository: SearchIndexRepository
    index_builder: SearchIndexBuilder
    tokenizer: Tokenizer
    post_repository: PostRepository

    def execute(self, query: str, user_id: UserId) -> List[PostId]:
        user_index = self.index_repository.get_index_by_user_id(user_id)
        if user_index is None:
            posts = self.post_repository.get_posts_by_user_id(user_id)
            user_index = self.index_builder.build_index(posts, self.tokenizer)
            self.index_repository.save_user_index(user_id, user_index)
        matches = self.index_lookup.lookup(query, user_index)
        return matches
