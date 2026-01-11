from typing import List

from fastapi.testclient import TestClient
from fastapi import Query

from infrastructure.fastapi.fastapi import AppBuilder
from infrastructure.fastapi.get_most_popular_authors_api import (
    GetPopularAuthorsAPIBase,
)
from infrastructure.fastapi.search_posts_api import SearchPostsAPIBase
from infrastructure.fastapi.compute_projection_api import ComputeProjectionAPIBase
from infrastructure.fastapi.compute_word_cloud_api import (
    ComputeWordCloudAPIBase,
)
from domain.entities.post import PostId, Post
from domain.entities.author import AuthorPopularity
from domain.entities.post import PostProjection


class DummyPopular(GetPopularAuthorsAPIBase):
    async def get_popular_authors(self):
        return [AuthorPopularity(author="Alice", post_count=3)]


class DummySearch(SearchPostsAPIBase):
    async def search_posts(self, query: str):
        return ["post_1", "post_2"]


class DummyProjection(ComputeProjectionAPIBase):
    async def compute_projection(self):
        return [PostProjection(post_id="post_1", x=0.1, y=0.2, keywords=[])]


class DummyWordCloud(ComputeWordCloudAPIBase):
    async def compute_word_cloud(self) -> bytes:
        return b"imagebytes"


class DummySave:
    async def save_posts(self, posts: list[Post]) -> None:
        # echo back the payload
        return posts


class DummyGet:
    async def get_posts(self, ids: List[PostId] = Query(None)) -> List[Post]:
        # ids expected as comma separated values in query params
        return [
            Post(
                id=pid,
                userId="user1",
                author="Author",
                authorImage="",
                authorHeadline="",
                timestamp="",
                text="",
                postImage="",
                profileUrl="",
                postUrl="",
                meta={},
            ) for pid in ids
        ]


def test_app_builder_creates_working_app():
    builder = AppBuilder(
        get_popular_authors_api=DummyPopular(),
        search_posts_api=DummySearch(),
        compute_projection_api=DummyProjection(),
        compute_word_cloud_api=DummyWordCloud(),
        save_posts_api=DummySave(),
        get_posts_api=DummyGet(),
    )

    app = builder.create_app()
    with TestClient(app) as client:
        r = client.get("/popular_authors")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

        r = client.get("/search", params={"query": "anything"})
        assert r.status_code == 200
        assert r.json() == ["post_1", "post_2"]

        r = client.get("/projection")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

        r = client.get("/wordcloud")
        assert r.status_code == 200
        assert isinstance(r.content, bytes)

        # POST /posts - save
        payload = [{"id": "1", "userId": "10", "author": "Bob", "authorImage": "", "authorHeadline": "", "timestamp": "", "text": "Hello", "postImage": "", "postUrl": "", "profileUrl": "", "meta": {}}]
        r = client.post("/users/me/posts", json=payload)
        print(r.json())
        assert r.status_code == 200
        assert r.json() == payload

        # GET /posts - retrieve
        r = client.get("/users/me/posts", params={"ids": ["p1", "p2"]})
        print(r.json())
        assert r.status_code == 200
        assert r.json() == [
            {"id": "p1", "userId": "user1", "author": "Author", "authorImage": "", "authorHeadline": "", "timestamp": "", "text": "", "postImage": "", "postUrl": "", "profileUrl": "", "meta": {}},
            {"id": "p2", "userId": "user1", "author": "Author", "authorImage": "", "authorHeadline": "", "timestamp": "", "text": "", "postImage": "", "postUrl": "", "profileUrl": "", "meta": {}},
        ]
