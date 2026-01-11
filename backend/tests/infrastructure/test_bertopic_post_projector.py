import pytest
from unittest.mock import MagicMock

import numpy as np
import umap

from domain.entities.post import Post, PostId
from infrastructure.bertopic_post_projector import BertopicPostProjector
from infrastructure import bertopic_post_projector


@pytest.fixture
def sample_posts():
    return [
        Post(
            id=PostId("1"),
            userId="1",
            author="A",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about AI",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("2"),
            userId="2",
            author="B",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about ML",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("3"),
            userId="3",
            author="C",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about Data Science",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("4"),
            userId="4",
            author="D",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about Deep Learning",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("5"),
            userId="5",
            author="E",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about NLP",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("6"),
            userId="6",
            author="F",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about Computer Vision",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("7"),
            userId="7",
            author="G",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about Reinforcement Learning",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("8"),
            userId="8",
            author="H",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about Generative Models",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("9"),
            userId="9",
            author="I",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about Transformers",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
        Post(
            id=PostId("10"),
            userId="10",
            author="J",
            authorImage="",
            authorHeadline="",
            timestamp="",
            text="Post about Graph Neural Networks",
            postImage="",
            postUrl="",
            profileUrl="",
            meta={},
        ),
    ]


class TestBertopicProjector:
    def test_project_returns_projections(self, monkeypatch, sample_posts):
        # Use MagicMock for embedder and set encode return value
        embedder_mock = MagicMock()
        embedder_mock.encode.return_value = np.array([[1.0, 2.0]] * len(sample_posts))

        # Use MagicMock for umap_model and set fit_transform return value
        umap_model_mock = MagicMock()
        umap_mock = MagicMock()
        umap_mock.UMAP.return_value = umap_model_mock
        umap_model_mock.fit_transform.return_value = np.array([[1.0, 2.0]] * len(sample_posts))
        umap_model_mock.embedding_ = np.array([[1.0, 2.0]] * len(sample_posts))
        monkeypatch.setattr(bertopic_post_projector, "umap", umap_mock)

        projector = BertopicPostProjector(
            embedder=embedder_mock,
            umap_n_components=2,
        )
        projections = projector.project(sample_posts)

        assert len(projections) == 10
        for proj in projections:
            assert proj.x == 1.0
            assert proj.y == 2.0
            assert len(proj.keywords) >= 0

    def test_project_with_real_bertopic(self, sample_posts):
        # Set n_neighbors=2 for UMAP to avoid k >= N and n_neighbors > 1 errors with 6 samples
        # Set min_dist=0.1 and n_components=2
        # Set n_epochs=10 to avoid UMAP warnings for small datasets
        projector = BertopicPostProjector(
            umap_n_components=2,
        )
        projections = projector.project(sample_posts)
        assert len(projections) == 10
        for proj in projections:
            assert isinstance(proj.x, float)
            assert isinstance(proj.y, float)
            assert isinstance(proj.keywords, list)
            assert all(hasattr(kw, 'keyword') and hasattr(kw, 'score') for kw in proj.keywords)
