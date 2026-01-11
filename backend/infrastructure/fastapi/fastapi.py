from dataclasses import dataclass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.fastapi.get_most_popular_authors_api import GetPopularAuthorsAPIBase
from infrastructure.fastapi.search_posts_api import SearchPostsAPIBase
from infrastructure.fastapi.compute_projection_api import ComputeProjectionAPIBase
from infrastructure.fastapi.compute_word_cloud_api import ComputeWordCloudAPIBase
from infrastructure.fastapi.save_posts_api import SavePostsAPIBase
from infrastructure.fastapi.get_posts_api import GetPostsAPIBase
from typing import Any


@dataclass
class AppBuilder:
    get_popular_authors_api: GetPopularAuthorsAPIBase = None
    search_posts_api: SearchPostsAPIBase = None
    compute_projection_api: ComputeProjectionAPIBase = None
    compute_word_cloud_api: ComputeWordCloudAPIBase = None
    save_posts_api: SavePostsAPIBase = None
    get_posts_api: GetPostsAPIBase = None

    def register_popular_authors_routes(self, app: FastAPI):
        """Register popular authors routes."""
        app.get("/popular_authors")(self.get_popular_authors_api.get_popular_authors)

    def register_search_posts_routes(self, app: FastAPI):
        app.get("/search")(self.search_posts_api.search_posts)

    def register_projection_routes(self, app: FastAPI):
        app.get("/projection")(self.compute_projection_api.compute_projection)

    def register_word_cloud_routes(self, app: FastAPI):
        app.get("/wordcloud")(self.compute_word_cloud_api.compute_word_cloud)

    def register_save_posts_routes(self, app: FastAPI):
        app.post("/users/me/posts")(self.save_posts_api.save_posts)

    def register_get_post_routes(self, app: FastAPI):
        app.get("/users/me/posts/{post_id}")(self.get_posts_api.get_post)

    def register_get_posts_routes(self, app: FastAPI):
        app.get("/users/me/posts")(self.get_posts_api.get_posts)

    def create_app(self) -> FastAPI:
        """Create and configure the FastAPI app with the given agent caller use case."""
        # Create the FastAPI instance
        app = FastAPI(title="LinkedIn Saved Posts Analyzer", version="1.0.0")

        # Register exception handlers
        # @app.exception_handler(SessionAlreadyExistsError)
        # async def session_already_exists_handler(
        #     request: Request,  # noqa: ARG001
        #     exc: SessionAlreadyExistsError,
        # ):
        #     return JSONResponse(
        #         status_code=409,
        #         content={"detail": str(exc), "session_id": exc.session_id},
        #     )

        # @app.exception_handler(SessionNotFoundError)
        # async def session_not_found_handler(
        #     request: Request,  # noqa: ARG001
        #     exc: SessionNotFoundError,
        # ):
        #     return JSONResponse(
        #         status_code=404,
        #         content={"detail": str(exc), "session_id": exc.session_id},
        #     )

        # Register routes
        if self.get_popular_authors_api:
            self.register_popular_authors_routes(app)
        if self.search_posts_api:
            self.register_search_posts_routes(app)
        if self.compute_projection_api:
            self.register_projection_routes(app)
        if self.compute_word_cloud_api:
            self.register_word_cloud_routes(app)
        if self.save_posts_api:
            self.register_save_posts_routes(app)
        if self.get_posts_api:
            self.register_get_posts_routes(app)


        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"], # FIXME: adjust for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        return app