import json
from pathlib import Path
from domain.entities.search import Post
from infrastructure.simple_tokenizer import SimpleTokenizer
from backend.infrastructure.search_index_builder import InMemorySearchIndex
from infrastructure.simple_snippet_builder import SimpleSnippetBuilder
from application.use_cases.search_posts import SearchPosts

# Load posts from JSON
json_path = Path("playground/linkedin-saved-posts.json")
with open(json_path, encoding="utf-8") as f:
    data = json.load(f)

posts = [Post(id=str(i), text=post.get("text", "")) for i, post in enumerate(data)]
posts_by_id = {p.id: p for p in posts}

tokenizer = SimpleTokenizer()
index = InMemorySearchIndex(posts, tokenizer)
snippet_builder = SimpleSnippetBuilder(posts_by_id)
search_engine = SearchPosts(index, tokenizer, snippet_builder)

# Example usage
def search_and_print(query):
    results = search_engine.execute(query)
    for r in results[:10]:
        print(f"Post ID: {r.post_id} | Score: {r.score}\nSnippet: {r.snippet}\n---")

# Example: search_and_print("AI marketing")
search_and_print("AI marketing")
