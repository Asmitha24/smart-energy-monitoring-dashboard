"""Tests for the Flask application."""
import pytest
from app import app  # Import your Flask app instance

@pytest.fixture()
def get_client():
    """
    Fixture to create a test client for the Flask app.
    Allows simulating requests without running a full server.
    """
    with app.test_client() as client:
        yield client

def test_index_route(get_client):
    """
    Test the main index route ('/').
    Checks for a 200 status code and expected content.
    """
    response = get_client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data
