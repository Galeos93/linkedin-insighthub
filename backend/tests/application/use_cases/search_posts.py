import pytest
from unittest.mock import Mock
from typing import List

from application.use_cases.search_posts import SearchPosts
from domain.entities.user_id import UserId
from domain.entities.post import Post, PostId
from infrastructure.search_index_builder import InMemorySearchIndexBuilder
from infrastructure.search_index_looker import SimpleSearchIndexLookup
from infrastructure.simple_tokenizer import SimpleTokenizer
from infrastructure.post_repository import InMemoryPostRepository
from infrastructure.search_index_repository import InMemorySearchIndexRepository


@pytest.fixture
def user_id() -> UserId:
    """Create a sample user ID."""
    return UserId("user_123")


@pytest.fixture
def sample_posts() -> List[Post]:
    """Create sample posts for testing."""
    return [
        Post(
            id=PostId("post_1"),
            userId=UserId("user_123"),
            author="Author One",
            authorImage="image1.jpg",
            authorHeadline="Headline 1",
            timestamp="2024-01-01",
            text="This is a Python programming post",
            postImage="post1.jpg",
        ),
        Post(
            id=PostId("post_2"),
            userId=UserId("user_123"),
            author="Author Two",
            authorImage="image2.jpg",
            authorHeadline="Headline 2",
            timestamp="2024-01-02",
            text="This is a Java programming post",
            postImage="post2.jpg",
        ),
        Post(
            id=PostId("post_3"),
            userId=UserId("user_123"),
            author="Author Three",
            authorImage="image3.jpg",
            authorHeadline="Headline 3",
            timestamp="2024-01-03",
            text="This is a web development post",
            postImage="post3.jpg",
        ),
    ]


@pytest.fixture
def mock_index_lookup() -> Mock:
    """Create a mock SearchIndexLookup."""
    return Mock()


@pytest.fixture
def mock_index_repository() -> Mock:
    """Create a mock SearchIndexRepository."""
    return Mock()


@pytest.fixture
def mock_index_builder() -> Mock:
    """Create a mock SearchIndexBuilder."""
    return Mock()


@pytest.fixture
def mock_tokenizer() -> Mock:
    """Create a mock Tokenizer."""
    return Mock()


@pytest.fixture
def mock_post_repository() -> Mock:
    """Create a mock PostRepository."""
    return Mock()


@pytest.fixture
def search_posts(
    mock_index_lookup,
    mock_index_repository,
    mock_index_builder,
    mock_tokenizer,
    mock_post_repository,
) -> SearchPosts:
    """Create a SearchPosts instance with mocked dependencies."""
    return SearchPosts(
        index_lookup=mock_index_lookup,
        index_repository=mock_index_repository,
        index_builder=mock_index_builder,
        tokenizer=mock_tokenizer,
        post_repository=mock_post_repository,
    )


class TestSearchPosts:
    """Test suite for SearchPosts use case."""

    def test_execute_with_existing_index(
        self, search_posts, user_id, mock_index_repository, mock_index_lookup
    ):
        """Test execute when index already exists for user."""
        # Arrange
        query = "Python"
        existing_index = {"key": [0, 1]}
        expected_matches = [0, 1]

        mock_index_repository.get_index_by_user_id.return_value = existing_index
        mock_index_lookup.lookup.return_value = expected_matches

        # Act
        result = search_posts.execute(query, user_id)

        # Assert
        assert result == expected_matches
        mock_index_repository.get_index_by_user_id.assert_called_once_with(user_id)
        mock_index_lookup.lookup.assert_called_once_with(query, existing_index)
        search_posts.post_repository.get_posts_by_user_id.assert_not_called()
        search_posts.index_builder.build_index.assert_not_called()
        mock_index_repository.save_user_index.assert_not_called()

    def test_execute_without_existing_index(
        self,
        search_posts,
        user_id,
        sample_posts,
        mock_index_repository,
        mock_index_builder,
        mock_tokenizer,
        mock_index_lookup,
    ):
        """Test execute when index doesn't exist and needs to be built."""
        # Arrange
        query = "programming"
        built_index = {"built": [0, 1]}
        expected_matches = [0, 1]

        mock_index_repository.get_index_by_user_id.return_value = None
        search_posts.post_repository.get_posts_by_user_id.return_value = sample_posts
        mock_index_builder.build_index.return_value = built_index
        mock_index_lookup.lookup.return_value = expected_matches

        # Act
        result = search_posts.execute(query, user_id)

        # Assert
        assert result == expected_matches
        mock_index_repository.get_index_by_user_id.assert_called_once_with(user_id)
        search_posts.post_repository.get_posts_by_user_id.assert_called_once_with(
            user_id
        )
        mock_index_builder.build_index.assert_called_once_with(
            sample_posts, mock_tokenizer
        )
        mock_index_repository.save_user_index.assert_called_once_with(user_id, built_index)
        mock_index_lookup.lookup.assert_called_once_with(query, built_index)

    def test_execute_returns_correct_matches(
        self, search_posts, user_id, mock_index_repository, mock_index_lookup
    ):
        """Test that execute returns the matches from lookup."""
        # Arrange
        query = "test query"
        existing_index = {}
        expected_matches = [0, 1, 2]

        mock_index_repository.get_index_by_user_id.return_value = existing_index
        mock_index_lookup.lookup.return_value = expected_matches

        # Act
        result = search_posts.execute(query, user_id)

        # Assert
        assert result == expected_matches
        assert len(result) == 3

    def test_execute_with_empty_query(
        self, search_posts, user_id, mock_index_repository, mock_index_lookup
    ):
        """Test execute with an empty query string."""
        # Arrange
        query = ""
        existing_index = {}
        expected_matches = []

        mock_index_repository.get_index_by_user_id.return_value = existing_index
        mock_index_lookup.lookup.return_value = expected_matches

        # Act
        result = search_posts.execute(query, user_id)

        # Assert
        assert result == expected_matches
        mock_index_lookup.lookup.assert_called_once_with(query, existing_index)

    def test_execute_with_no_matching_results(
        self, search_posts, user_id, mock_index_repository, mock_index_lookup
    ):
        """Test execute when no posts match the query."""
        # Arrange
        query = "nonexistent_keyword"
        existing_index = {}
        expected_matches = []

        mock_index_repository.get_index_by_user_id.return_value = existing_index
        mock_index_lookup.lookup.return_value = expected_matches

        # Act
        result = search_posts.execute(query, user_id)

        # Assert
        assert result == []
        mock_index_lookup.lookup.assert_called_once_with(query, existing_index)

    def test_execute_builds_index_only_once(
        self,
        search_posts,
        user_id,
        sample_posts,
        mock_index_repository,
        mock_index_builder,
        mock_tokenizer,
        mock_index_lookup,
    ):
        """Test that index is built and saved exactly once when it doesn't exist."""
        # Arrange
        query = "search"
        built_index = {"built": "index"}
        mock_index_repository.get_index_by_user_id.return_value = None
        search_posts.post_repository.get_posts_by_user_id.return_value = sample_posts
        mock_index_builder.build_index.return_value = built_index
        mock_index_lookup.lookup.return_value = ["match"]

        # Act
        search_posts.execute(query, user_id)

        # Assert
        mock_index_builder.build_index.assert_called_once()
        mock_index_repository.save_user_index.assert_called_once()

    def test_execute_passes_correct_parameters_to_dependencies(
        self,
        search_posts,
        user_id,
        sample_posts,
        mock_index_repository,
        mock_index_builder,
        mock_tokenizer,
        mock_index_lookup,
    ):
        """Test that execute passes correct parameters to all dependencies."""
        # Arrange
        query = "specific query"
        built_index = {"index": "data"}

        mock_index_repository.get_index_by_user_id.return_value = None
        search_posts.post_repository.get_posts_by_user_id.return_value = sample_posts
        mock_index_builder.build_index.return_value = built_index
        mock_index_lookup.lookup.return_value = []

        # Act
        search_posts.execute(query, user_id)

        # Assert
        mock_index_repository.get_index_by_user_id.assert_called_with(user_id)
        search_posts.post_repository.get_posts_by_user_id.assert_called_with(user_id)
        mock_index_builder.build_index.assert_called_with(sample_posts, mock_tokenizer)
        mock_index_repository.save_user_index.assert_called_with(user_id, built_index)
        mock_index_lookup.lookup.assert_called_with(query, built_index)

    def test_execute_with_special_characters_in_query(
        self, search_posts, user_id, mock_index_repository, mock_index_lookup
    ):
        """Test execute with special characters in the query."""
        # Arrange
        query = "C++ && Python || Java?"
        existing_index = {}
        expected_matches = ["post_1"]

        mock_index_repository.get_index_by_user_id.return_value = existing_index
        mock_index_lookup.lookup.return_value = expected_matches

        # Act
        result = search_posts.execute(query, user_id)

        # Assert
        assert result == expected_matches
        mock_index_lookup.lookup.assert_called_once_with(query, existing_index)

    def test_execute_preserves_query_string(
        self, search_posts, user_id, mock_index_repository, mock_index_lookup
    ):
        """Test that the query string is passed unchanged to lookup."""
        # Arrange
        queries = ["Python", "PYTHON", "python", "PyThOn"]
        existing_index = {"key": [0, 1]}

        mock_index_repository.get_index_by_user_id.return_value = existing_index
        mock_index_lookup.lookup.return_value = []

        # Act & Assert
        for query in queries:
            search_posts.execute(query, user_id)
            mock_index_lookup.lookup.assert_called_with(query, existing_index)

    def test_execute_with_different_user_ids(
        self, search_posts, mock_index_repository, mock_index_lookup, sample_posts
    ):
        """Test execute maintains separate indices for different users."""
        # Arrange
        user_id_1 = UserId("user_1")
        user_id_2 = UserId("user_2")
        query = "search"
        index_1 = {"user": "1"}
        index_2 = {"user": "2"}

        mock_index_repository.get_index_by_user_id.side_effect = [index_1, index_2]
        mock_index_lookup.lookup.return_value = ["match"]

        # Act
        search_posts.execute(query, user_id_1)
        search_posts.execute(query, user_id_2)

        # Assert
        assert mock_index_repository.get_index_by_user_id.call_count == 2
        mock_index_repository.get_index_by_user_id.assert_any_call(user_id_1)
        mock_index_repository.get_index_by_user_id.assert_any_call(user_id_2)
        assert mock_index_lookup.lookup.call_count == 2

    @pytest.mark.parametrize(
        "looker,builder,tokenizer,post_repo,index_repo",
        [
            (
                SimpleSearchIndexLookup(tokenizer=SimpleTokenizer()),
                InMemorySearchIndexBuilder(),
                SimpleTokenizer(),
                InMemoryPostRepository(),
                InMemorySearchIndexRepository(),
            ),
        ],
    )
    def test_integration_execute(
        self,
        looker,
        builder,
        tokenizer,
        post_repo,
        index_repo,
        user_id,
        sample_posts,
    ):
        """Integration test for SearchPosts with real implementations."""
        # Arrange
        search_posts = SearchPosts(
            index_lookup=looker,
            index_repository=index_repo,
            index_builder=builder,
            tokenizer=tokenizer,
            post_repository=post_repo,
        )
        query = "programming"

        for post in sample_posts:
            post_repo.add_post(post)

        # Act
        results = search_posts.execute(query, user_id)

        # Assert
        assert len(results) == 2  # Expecting 2 posts related to programming
