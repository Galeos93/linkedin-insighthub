from typing import List, Tuple, Dict

from domain.entities.search import SearchResult, Post


class SimpleSnippetBuilder:
    def __init__(self, posts_by_id: Dict[str, Post]):
        self.posts = posts_by_id

    def build(self, matches: List[Tuple[str, float]], tokens: List[str]) -> List[SearchResult]:
        results = []
        for post_id, score in matches:
            text = self.posts[post_id].text
            snippet = self._make_snippet(text, tokens)
            results.append(SearchResult(post_id, score, snippet))
        return results

    def _make_snippet(self, text: str, tokens: List[str]) -> str:
        for token in tokens:
            idx = text.lower().find(token)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(text), idx + 40)
                return text[start:end]
        return text[:80]
