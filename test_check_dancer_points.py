"""Tests for check_dancer_points.py."""
from typing import Generator
import pytest
from flask.testing import FlaskClient
from check_dancer_points import app


@pytest.fixture()
def client() -> Generator[FlaskClient, None, None]:
    """Create a fresh flask client for a function."""
    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        yield client
        ctx.pop()


def test_no_name_or_id(client: FlaskClient) -> None:
    """Test that no name or ID provided returns an error."""
    response = client.get("/")
    assert response.json == {"error": "No name or ID provided."}


def test_no_results(client: FlaskClient) -> None:
    """Test that no results found returns an error."""
    response = client.get("/?name_or_id=not%20a%20dancer")
    assert response.json == {"error": "No results found."}


def test_name_and_id(client: FlaskClient) -> None:
    """Test that name and ID are returned."""
    response = client.get("/?name_or_id=Theodore%20Williams")  # That's me!
    assert response.json["name"] == "Theodore Williams"  # type: ignore[index]
    assert response.json["id"] == 11612  # type: ignore[index]
