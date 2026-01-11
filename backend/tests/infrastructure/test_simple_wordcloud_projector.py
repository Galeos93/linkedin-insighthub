import pytest
from domain.entities.post import Post
from infrastructure.simple_wordcloud_projector import SimpleWordCloudProjector, WordCloudFormat

@pytest.fixture
def posts():
    return [
        Post(
            id="1",
            userId="1",
            author="A",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="AI marketing healthcare",
            postImage="",
            profileUrl="",
            postUrl="",
            meta={},
        ),
        Post(id="2", userId="1", author="B", authorImage="", authorHeadline="", timestamp="", text="AI finance education", postImage="", profileUrl="", postUrl="", meta={}),
    ]

class TestSimpleWordCloudProjector:
    @staticmethod
    def test_wordcloud_jpeg(posts):
        projector = SimpleWordCloudProjector(format=WordCloudFormat.JPEG)
        img_bytes = projector.compute_word_cloud(posts)
        assert isinstance(img_bytes, bytes)
        assert img_bytes[:2] == b'\xff\xd8'  # JPEG magic number

    @staticmethod
    def test_wordcloud_png(posts):
        projector = SimpleWordCloudProjector(format=WordCloudFormat.PNG)
        img_bytes = projector.compute_word_cloud(posts)
        assert isinstance(img_bytes, bytes)
        assert img_bytes[:8] == b'\x89PNG\r\n\x1a\n'  # PNG magic number

    @staticmethod
    def test_wordcloud_svg(posts):
        projector = SimpleWordCloudProjector(format=WordCloudFormat.SVG)
        img_bytes = projector.compute_word_cloud(posts)
        assert isinstance(img_bytes, bytes)
        assert img_bytes.strip().startswith(b'<svg')

    @staticmethod
    def test_wordcloud_empty_posts():
        projector = SimpleWordCloudProjector()
        with pytest.raises(ValueError):
            projector.compute_word_cloud([])

    @staticmethod
    def test_wordcloud_bad_format(posts):
        class BadFormat:
            value = 'bmp'
        projector = SimpleWordCloudProjector(format=BadFormat)
        with pytest.raises(ValueError):
            projector.compute_word_cloud(posts)
