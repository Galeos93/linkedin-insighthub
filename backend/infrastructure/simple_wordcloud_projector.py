from io import BytesIO
from dataclasses import dataclass, field
from hashlib import sha256
from enum import Enum
import re

from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords

from domain.entities.post import Post
from application.interfaces.post_wordcloud_projector import PostWordCloudProjector


class WordCloudFormat(Enum):
    JPEG = 'jpeg'
    PNG = 'png'
    SVG = 'svg'


@dataclass
class SimpleWordCloudProjector(PostWordCloudProjector):
    width: int = 400
    height: int = 200
    background_color: str = 'white'
    format: WordCloudFormat = WordCloudFormat.PNG
    languages: list[str] = None
    _cache: dict[str, bytes] = field(default_factory=dict, init=False, repr=False)

    def _cache_key(self, posts: list[Post]) -> str:
        """Generate a cache key based on post IDs and format."""
        post_ids = '-'.join(sorted(str(post.id) for post in posts))
        key = f"{post_ids}-{self.format.value}-{self.width}x{self.height}"
        return sha256(key.encode('utf-8')).hexdigest()

    @staticmethod
    def _compute_stopwords(languages: list[str] | None) -> set[str]:
        all_stopwords = set(STOPWORDS)
        if languages is None:
            langs = stopwords.fileids()
        else:
            langs = languages
        for lang in langs:
            try:
                all_stopwords.update(stopwords.words(lang))
            except OSError:
                raise ValueError(f"Stopwords for language '{lang}' not found in NLTK corpus.")
        return all_stopwords

    def compute_word_cloud(self, posts: list[Post]) -> bytes:
        if not posts:
            raise ValueError("No posts provided for word cloud generation.")

        # Check cache first
        cache_key = self._cache_key(posts)
        if cache_key in self._cache:
            return self._cache[cache_key]

        texts = ' '.join([post.text for post in posts])
        # Remove URLs from the text
        texts = re.sub(r'https?://\S+|www\.\S+', '', texts)

        # Collect stopwords from all specified languages, or all if languages is None
        all_stopwords = self._compute_stopwords(self.languages)

        if self.format not in WordCloudFormat:
            raise ValueError(
                f"Unsupported format: {self.format}. Allowed formats are:"
                f" {[f.value for f in WordCloudFormat]}"
            )

        wc = WordCloud(
            width=self.width,
            height=self.height,
            background_color=self.background_color,
            stopwords=all_stopwords
        ).generate(texts)

        img_bytes = BytesIO()
        if self.format == WordCloudFormat.SVG:
            img_bytes.write(wc.to_svg().encode('utf-8'))
        else:
            wc.to_image().save(img_bytes, format=self.format.value.upper())

        # Store in cache
        self._cache[cache_key] = img_bytes.getvalue()
        return self._cache[cache_key]
