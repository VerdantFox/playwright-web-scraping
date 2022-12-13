"""Tests for check_dancer_points.py."""
import pytest
from pytest import MonkeyPatch
from flask.testing import FlaskClient
from check_dancer_points import app
import check_dancer_points


@pytest.fixture()
def client() -> FlaskClient:
    """Create a fresh flask client for a function."""
    return app.test_client()


def test_no_name_or_id(client: FlaskClient) -> None:
    """Test that no name or ID provided returns an error."""
    response = client.get("/")
    assert response.json == {"error": "No name or ID provided."}


def test_no_results(client: FlaskClient, monkeypatch: MonkeyPatch) -> None:
    """Test that no results found returns an error."""
    monkeypatch.setattr(check_dancer_points, "TIMEOUT", 1)
    response = client.get("/?name_or_id=not%20a%20dancer")
    assert response.json == {"error": "No results found."}


def test_name_and_id(client: FlaskClient) -> None:
    """Test that name and ID are returned."""
    response = client.get("/?name_or_id=Theodore%20Williams")  # That's me!
    assert response.json and "error" not in response.json
    assert response.json["name"] == "Theodore Williams"
    assert response.json["id"] == 11612
