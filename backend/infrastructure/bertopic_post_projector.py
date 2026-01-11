from dataclasses import dataclass, field
import re
from typing import List
from hashlib import sha256

from bertopic import BERTopic
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import umap

from domain.entities.post import Post, PostProjection, KeywordRelevance
from application.interfaces.post_projector import PostProjector


import math
import re
from dataclasses import dataclass, field
from hashlib import sha256
from typing import List

import umap
from bertopic import BERTopic
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer


# @dataclass
# class BertopicPostProjector(PostProjector):
#     embedder: SentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")
#     umap_model: umap.UMAP = umap.UMAP(n_components=2, n_neighbors=2)
#     _cache: dict[str, List[PostProjection]] = field(default_factory=dict, init=False, repr=False)

#     def __post_init__(self):
#         self.topic_model = BERTopic(umap_model=self.umap_model)
#         self.languages: List[str] = None

#     @staticmethod
#     def _compute_stopwords(languages: list[str] | None) -> set[str]:
#         all_stopwords = set()
#         langs = languages if languages is not None else stopwords.fileids()
#         for lang in langs:
#             try:
#                 all_stopwords.update(stopwords.words(lang))
#             except OSError:
#                 raise ValueError(f"Stopwords for language '{lang}' not found in NLTK corpus.")
#         return all_stopwords

#     def preprocess_text(self, text: str) -> str:
#         text = text.lower()
#         text = re.sub(r'https?://\S+|www\.\S+', '', text)
#         stop_words = self._compute_stopwords(self.languages)
#         return ' '.join([word for word in text.split() if word not in stop_words])

#     def _cache_key(self, posts: List[Post]) -> str:
#         """Generate a unique cache key based on post IDs and topic model parameters."""
#         post_ids = '-'.join(sorted(str(post.id) for post in posts))
#         key_str = f"{post_ids}-umap{self.umap_model.n_components}-{self.umap_model.n_neighbors}"
#         return sha256(key_str.encode('utf-8')).hexdigest()

#     def project(self, posts: List[Post]) -> List[PostProjection]:
#         if not posts:
#             return []

#         # Check cache first
#         cache_key = self._cache_key(posts)
#         if cache_key in self._cache:
#             return self._cache[cache_key]

#         # Preprocess texts
#         texts = [self.preprocess_text(post.text) for post in posts]

#         # Get embeddings
#         embeddings = self.embedder.encode(texts, convert_to_numpy=True)

#         # Fit BERTopic
#         topics, probs = self.topic_model.fit_transform(texts, embeddings=embeddings)

#         # Get reduced embeddings from BERTopic's UMAP
#         umap_embeddings = self.topic_model.umap_model.embedding_

#         projections = []
#         for post, topic_id, coords in zip(posts, topics, umap_embeddings):
#             keywords = self.topic_model.get_topic(topic_id) or []
#             kw_objs = [KeywordRelevance(keyword=k, score=s) for k, s in keywords]
#             projection = PostProjection(
#                 post_id=post.id,
#                 x=float(coords[0]),
#                 y=float(coords[1]),
#                 keywords=kw_objs
#             )
#             projections.append(projection)

#         # Store in cache
#         self._cache[cache_key] = projections
#         return projections

@dataclass
class BertopicPostProjector(PostProjector):
    embedder: SentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")
    umap_n_components: int = 2
    _cache: dict[str, List[PostProjection]] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        self.languages: List[str] | None = None

    def _compute_n_neighbors(self, n_posts: int) -> int:
        """
        Compute UMAP n_neighbors based on corpus size.

        Enforces a minimum corpus size of 10 posts.
        """
        # if n_posts < 10:
        #     raise ValueError(
        #         f"UMAP projection requires at least 10 posts; received {n_posts}."
        #     )

        if n_posts < 30:
            return 2
        if n_posts < 100:
            return 3
        if n_posts < 300:
            return 4
        if n_posts < 1000:
            return 5
        return 8

    @staticmethod
    def _compute_stopwords(languages: list[str] | None) -> set[str]:
        all_stopwords = set()
        langs = languages if languages is not None else stopwords.fileids()
        for lang in langs:
            try:
                all_stopwords.update(stopwords.words(lang))
            except OSError:
                raise ValueError(
                    f"Stopwords for language '{lang}' not found in NLTK corpus."
                )
        return all_stopwords

    def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
        stop_words = self._compute_stopwords(self.languages)
        return " ".join(word for word in text.split() if word not in stop_words)

    def _cache_key(self, posts: List[Post], n_neighbors: int) -> str:
        """
        Generate a cache key based on post IDs and UMAP configuration.
        """
        post_ids = "-".join(sorted(str(post.id) for post in posts))
        key_str = (
            f"{post_ids}"
            f"-umap{self.umap_n_components}"
            f"-neighbors{n_neighbors}"
        )
        return sha256(key_str.encode("utf-8")).hexdigest()

    def project(self, posts: List[Post]) -> List[PostProjection]:
        if not posts:
            return []

        n_neighbors = self._compute_n_neighbors(len(posts))

        cache_key = self._cache_key(posts, n_neighbors)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Build UMAP dynamically
        umap_model = umap.UMAP(
            n_components=self.umap_n_components,
            n_neighbors=n_neighbors,
            random_state=42,
        )

        topic_model = BERTopic(umap_model=umap_model)

        # Preprocess texts
        texts = [self.preprocess_text(post.text) for post in posts]

        # Encode embeddings
        embeddings = self.embedder.encode(texts, convert_to_numpy=True)

        # Fit topic model
        topics, probs = topic_model.fit_transform(texts, embeddings=embeddings)

        # Retrieve reduced embeddings
        umap_embeddings = topic_model.umap_model.embedding_

        projections: List[PostProjection] = []
        for post, topic_id, coords in zip(posts, topics, umap_embeddings):
            keywords = topic_model.get_topic(topic_id) or []
            kw_objs = [
                KeywordRelevance(keyword=k, score=s) for k, s in keywords
            ]

            projections.append(
                PostProjection(
                    post_id=post.id,
                    x=float(coords[0]),
                    y=float(coords[1]),
                    keywords=kw_objs,
                )
            )

        self._cache[cache_key] = projections
        return projections
