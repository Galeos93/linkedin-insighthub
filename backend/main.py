"""Startup script for the LinkedIn Saved Posts analyzer application.

This script initializes and runs the FastAPI app with clean architecture setup.
"""

import logging
from pathlib import Path

from dotenv import load_dotenv
import uvicorn
from vyper import v

from application.use_cases.search_posts import SearchPosts
from application.use_cases.get_popular_authors import GetPopularAuthors
from application.use_cases.compute_projection import ComputeProjection
from application.use_cases.compute_word_cloud import ComputeWordCloud
from application.use_cases.get_posts import GetPostsUseCase
from application.use_cases.save_posts import SavePostsUseCase
from infrastructure.fastapi.fastapi import AppBuilder
from infrastructure.fastapi.search_posts_api import SearchPostsAPIImpl
from infrastructure.fastapi.get_most_popular_authors_api import GetPopularAuthorsAPIImpl
from infrastructure.fastapi.compute_projection_api import ComputeProjectionAPIImpl
from infrastructure.fastapi.compute_word_cloud_api import ComputeWordCloudAPIImpl
from infrastructure.fastapi.save_posts_api import SavePostsAPIImpl
from infrastructure.fastapi.get_posts_api import GetPostsAPIImpl
from infrastructure.post_repository import InMemoryPostRepository
from infrastructure.simple_author_ranker import SimpleAuthorRanker
from infrastructure.simple_tokenizer import SimpleTokenizer
from infrastructure.search_index_builder import InMemorySearchIndexBuilder
from infrastructure.search_index_looker import SimpleSearchIndexLookup
from infrastructure.search_index_repository import InMemorySearchIndexRepository
from infrastructure.bertopic_post_projector import BertopicPostProjector
from infrastructure.simple_wordcloud_projector import SimpleWordCloudProjector

logger = logging.getLogger(__name__)


def load_dotenv_config():
    """Load environment variables from .env file."""
    load_dotenv()


def load_vyper_config():
    """Load configuration files from paths."""
    logging.basicConfig(level=logging.INFO)
    logger.info("[Main] Loading vyper config")
    config_paths = [Path(".."), Path()]

    v.set_env_key_replacer(".", "_")

    v.set_config_type("yaml")
    v.set_config_name("config")

    for path in config_paths:
        v.add_config_path(path)
    try:
        v.read_in_config()  # Find and read the config file
    except Exception as e:
        logger.warning(
            "[Main] No configuration files found: %s",
            e,
        )

    v.automatic_env()
    logger.info(
        "[Main] Vyper config loaded: %s",
        v,
    )

    v.set_default("fastapi.host", "0.0.0.0")
    v.set_default("fastapi.port", 8000)
    v.set_default("fastapi.log_level", "info")
    v.set_default("fastapi.workers", 1)



def configure_app():
    """Configure the FastAPI app with all dependencies using clean architecture."""
    logger.info("Initializing infrastructure dependencies...")

    # Initialize repositories
    post_repository = InMemoryPostRepository()

    # Initialize search infrastructure
    tokenizer = SimpleTokenizer()
    search_index_builder = InMemorySearchIndexBuilder()
    search_index_repository = InMemorySearchIndexRepository()
    search_index_lookup = SimpleSearchIndexLookup(tokenizer=tokenizer)

    # Initialize author ranker
    author_ranker = SimpleAuthorRanker()

    # Initialize projectors
    post_projector = BertopicPostProjector()
    word_cloud_projector = SimpleWordCloudProjector()

    logger.info("Initializing use cases...")

    # Create use cases (Application Layer)
    search_posts_use_case = SearchPosts(
        index_lookup=search_index_lookup,
        index_repository=search_index_repository,
        index_builder=search_index_builder,
        tokenizer=tokenizer,
        post_repository=post_repository,
    )

    get_popular_authors_use_case = GetPopularAuthors(
        author_ranker=author_ranker,
        post_repository=post_repository,
    )

    compute_projection_use_case = ComputeProjection(
        post_repository=post_repository,
        post_projector=post_projector,
    )

    compute_word_cloud_use_case = ComputeWordCloud(
        post_repository=post_repository,
        post_wordcloud_projector=word_cloud_projector,
    )

    get_posts = GetPostsUseCase(
        post_repository=post_repository,
    )

    save_posts_use_case = SavePostsUseCase(
        post_repository=post_repository
    )

    logger.info("Creating API handlers...")

    # Create API handlers (Infrastructure Layer - FastAPI adapters)
    search_posts_api = SearchPostsAPIImpl(search_posts_use_case=search_posts_use_case)
    get_popular_authors_api = GetPopularAuthorsAPIImpl(
        get_popular_authors_use_case=get_popular_authors_use_case
    )
    compute_projection_api = ComputeProjectionAPIImpl(
        compute_projection_use_case=compute_projection_use_case
    )
    compute_word_cloud_api = ComputeWordCloudAPIImpl(
        compute_word_cloud_use_case=compute_word_cloud_use_case
    )
    save_posts_api = SavePostsAPIImpl(
        save_posts_use_case=save_posts_use_case
    )
    get_posts_api = GetPostsAPIImpl(
        get_posts_use_case=get_posts
    )

    logger.info("Building FastAPI application...")

    # Create FastAPI app using the AppBuilder
    app_builder = AppBuilder(
        search_posts_api=search_posts_api,
        get_popular_authors_api=get_popular_authors_api,
        compute_projection_api=compute_projection_api,
        compute_word_cloud_api=compute_word_cloud_api,
        save_posts_api=save_posts_api,
        get_posts_api=get_posts_api,
    )
    main_app = app_builder.create_app()

    return main_app


# Create the app at module level for uvicorn reload
logger.info("Loading configuration...")
load_dotenv_config()
load_vyper_config()
app = configure_app()


def main():
    """Implement entry point for the application."""
    print("🚀 Starting LinkedIn Saved Posts Analyzer API...")
    print("   - Search Posts: GET /search?query=<query>")
    print("   - Popular Authors: GET /popular_authors")
    print("   - Compute Projection: GET /projection")
    print("   - Word Cloud: GET /wordcloud")

    fastapi_host = v.get_string("fastapi.host")
    fastapi_port = v.get_int("fastapi.port")
    fastapi_log_level = v.get_string("fastapi.log_level")
    fastapi_workers = v.get_int("fastapi.workers")

    # Start the server using the module-level app
    uvicorn.run(
        "main:app",
        workers=fastapi_workers,
        host=fastapi_host,
        port=fastapi_port,
        log_level=fastapi_log_level,
        timeout_worker_healthcheck=60,
    )


if __name__ == "__main__":
    main()
